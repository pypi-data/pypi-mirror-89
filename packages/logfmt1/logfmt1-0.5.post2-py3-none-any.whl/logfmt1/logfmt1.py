# encoding: utf-8
# api: python
# title: python3-logfmt1
# description: handle *.log.fmt specifiers and regex conversion
# type: transform
# category: io
# version: 0.5-2
# license: Apache-2.0
# pack:
#    logfmt1.py=/usr/lib/python3/dist-packages/
#    update_logfmt.py=/usr/bin/update-logfmt
#    ./logex.py=/usr/bin/logex
#    share=/usr/share/logfmt
# architecture: all
# depends: python (>= 3.6)
# url: https://fossil.include-once.org/modseccfg/wiki/logfmt1
#
# Logging format strings to regex conversion.
#
# This is supposed to recognize .fmt files adjacent to logs,
# which document both the application type and log variant
# with the most current %p%l%ace%holder definition used.
# The purpose of this is to allow log extraction with exact
# matches using named fields, instead of cut/awk guesswork.
#
# Normally a .log file should have an adjacent .fmt file with:
#    {
#       "class": "appname variant",
#       "record": "%a %h %u [%t] %M"
#    }
#
# While the full conversion rules would be contained in a file
# within /usr/share/logfmt/appname.variant.fmt, containing:
#    {
#      "fields": { "%a": {id:…, rx:…} },
#      "alias": { "alias": "key", },
#      "placeholder": "%\w+",
#      "expand": { "%{pfx:(.+)}": {…} }
#
# Thus the regex can be built from the .log.fmt definition,
# and the placeholder to regex (or grok) conversion rules.
# A more specific definition file like 'apache.combined.fmt'
# might predeclare a default "record": placeholder string,
# which then is inherited through "class":"apache combined"
# without the .log.fmt having a record: line.
#
# Notably generates standard regex syntax (`$1` or `(?<name>`),
# so requires rx2re() to use the constructed regex: in Python.
#



import re, json, os, sys
from copy import copy


class rulesdb:

    # Known format strings and field identifiers.
    # This mixes both accesslog and errorlog format strings, should
    # be split out perhaps, as `%{cu}t` won't work in access.logs.
    #
    # - "[client %s:%d]" : "[remote %s:%d]" only in errorlogdefault?
    #
    apache = {
        "class": "apache generic",

        #"record": "%h %l %u %t \"%r\" %>s %b",

        #"regex": "(?<remote_host>\S+) …",

        "separator": " ",
        "rewrite": {
            "%[\d!,+\-]+": "%",      # strip Apache placehoder conditions
            "(?<!\\\\)([\[\]\|\(\)])": r"\\$1",  # escape any regex meta chars in format string
            "%%": "%",
        },
        "placeholder": "%[<>]?(?:\w*\{[^\}]+\})?\^?\w+",
        
        # placeholder definitions to build regex: from
        "fields": {
            "%a": { "id": "remote_addr", "rx": "[\d.:a-f]+", "type": "ip" },
            "%{c}a": { "id": "remote_addr", "rx": "[\d.:a-f]+", "type": "ip" },
            "%h": { "id": "remote_host", "rx": "[\w\-.:]+" },
            "%{c}h": { "id": "remote_host", "rx": "[\w\-.:]+" },
            "%A": { "id": "local_address", "rx": "[\d.:a-f]+", "type": "ip" },
            "%u": { "id": "remote_user", "rx": "[\-\w@.]+" },
            "%l": { "id": "remote_logname", "rx": "[\w\-.:]+" },   # %alias `loglevel` (errlog)
            "%t": { "id": "request_time", "rx": "\[?(\d[\d:\w\s:./\-+,;]+)\]?", "type": "datetime" }, # might be "local" formatting, e.g. [01/Mnt/2020:11:22:33 +0100], %alias `ctime`
            "%{u}t": { "id": "request_time", "rx": "u|\d+/\w+/\d+:\d+:\d+:\d+\.\d+\s\+\d+" },  # 01/Mnt/2020:11:22:33.12345 +0100 no implicit brackets
            "%{cu}t": { "id": "request_time", "rx": "ut|\d+-\w+-\d+\s\d+:\d+:\d+\.\d+" },  # error.log-only, 2020-01-31 11:22:33.901234, compact ISO 8601 format, no implicit brackets
            "%{msec_frac}t": { "id": "msec_frac", "rx": "[\d.]+" },
            "%{usec_frac}t": { "id": "usec_frac", "rx": "[\d.]+" },
            "%f": { "id": "request_file", "rx": "[^\s\"]+" },
            "%b": { "id": "bytes_sent", "rx": "\d+|-" },
            "%B": { "id": "bytes_sent", "rx": "\d+|-" },
            "%O": { "id": "bytes_out", "rx": "\d+", "type": "int" },
            "%I": { "id": "bytes_in", "rx": "\d+", "type": "int" },
            "%S": { "id": "bytes_combined", "rx": "\d+", "type": "int" },
            "%E": { "id": "apr_status", "rx": "\w+" },  # "AH01071"
            "%M": { "id": "message", "rx": ".+" }, # error.log-only, not really defined anywhere, ???
            "%L": { "id": "log_id", "rx": "[\w\-\.]+" },
            "%{c}L": { "id": "log_id", "rx": "[\w\-\.]+" },
            "%{C}L": { "id": "log_id", "rx": "[\w\-\.]*" },
            "%V": { "id": "server_name", "rx": "[\w\-\.]+" },
            "%v": { "id": "virtual_host", "rx": "[\w\-\.]+" },
            "%p": { "id": "server_port", "rx": "\d+", "type": "ip" },
            "%{local}p": { "id": "server_port", "rx": "\d+", "type": "int" },
            "%{canonical}p": { "id": "canonical_port", "rx": "[\w.]+" },
            "%{remote}p": { "id": "remote_port", "rx": "\d+" },
            "%P": { "id": "pid", "rx": "\d+", "type": "int" },
            "%{g}T": { "id": "tid", "rx": "\d+" },
            "%{tid}P": { "id": "tid", "rx": "\d+" },
            "%{pid}P": { "id": "pid", "rx": "\d+" },
            "%{hextid}P": { "id": "tid", "rx": "\w+" },
            "%{hexpid}P": { "id": "pid", "rx": "\w+" },
            "%H": { "id": "request_protocol", "rx": "[\w/\d.]+" },
            "%m": { "id": "request_method", "rx": "[\w.]+" }, # %alias `module_name` (errlog)
            "%q": { "id": "request_query", "rx": "\??\S*" },
            "%F": { "id": "file_line", "rx": "[/\w\-.:(\d)]+" }, # %alias `request_flushed`
            "%X": { "id": "connection_status", "rx": "[Xx+\-.\d]+" },
            "%k": { "id": "keepalives", "rx": "\d+" }, # %alias `requests_on_connection`
            "%r": { "id": "request_line", "rx": "(?<request_method>\w+) (?<request_path>\S+) (?<request_protocol>[\w/\d.]+)" },
            "%D": { "id": "request_duration_microseconds", "rx": "\d+", "type": "int" },
            "%T": { "id": "request_duration_scaled", "rx": "[\d.]+", "type": "float" },
            "%{s}T": { "id": "request_duration_seconds", "rx": "[\d.]+", "type": "float" },
            "%{us}T": { "id": "request_duration_microseconds", "rx": "\d+", "type": "int" },
            "%{ms}T": { "id": "request_duration_milliseconds", "rx": "\d+", "type": "int" },
            "%U": { "id": "request_uri", "rx": "\S+(?<!\")" },
            "%s": { "id": "status", "rx": "\d+", "type": "int" },
            "%>s": { "id": "status", "rx": "-|\d\d\d" },
            "%R": { "id": "handler", "rx": "[\w:.\-]+" },
            "%^FU": { "id": "ttfu", "rx": "-|\d+" },
            "%^FB": { "id": "ttfb", "rx": "-|\d+" },
            # Apache 2.5, flat key:value structure presumably
            "%^ĴS": { "id": "json", "rx": '\{(?:[\w:,\s\[\]]+|"(?:[^\\\\"]+|\\\\.)*")\}' },
            # common compound placeholders
            "%{Referer}i": { "id": "referer", "rx": "[^\"]*" },
            "%{User-Agent}i": { "id": "user_agent", "rx": r'(?:[^"]+|\\")*' },
        },
        "#doc": "https://httpd.apache.org/docs/2.4/mod/mod_log_config.html#formats",
        "#src": "https://github.com/apache/httpd/blob/trunk/modules/loggers/mod_log_config.c",

        # used by log extraction
        "alias": {
            "remote_address": "remote_addr",
            "ip": "remote_addr",
            "user": "remote_user",
            "file": "request_file",
            "size": "bytes_sent",
            "datetime": "request_time",
            "ctime": "request_time",
            "date": "request_time",
            "loglevel": "remote_logname",
            "module_name": "request_method",
            "request_flushed": "file_line",
            "requests_on_connection": "keepalives",
            "error": "apr_status",
            "request_flushed": "file_line",
        },

        # convert variant placeholders into fields beforehand,
        # possibly looking up other definitions (strftime) for marshalled placeholders
        "expand": {
            "%\{([^{}]+)\}t": {
                "id": "request_time",
                "class": "strftime", # different placeholders within \{...\}
                "record": "$1",
                "type": "datetime"
            },
            "%[<>]?\{([\w\-]+)\}[Conexic]": {
                "id": "$1",
                "rx": "\S+",
                "if_quoted": "(?:[^\"]*|\\\\\")+",
            },
            "%\{([\w\-]+)\}\^t[io]": {
                "id": "$1",
                "rx": "\S+"
            },
        },

        # post-process field to split out key-value pair formats
        "container": {
            "message": {
                "id": "$1", "value": "$2",
                "rx": "\[(\w+) \"(.*?)\"\]",
                "class": "apache mod_security"
            }
        },

        # which log files to apply on, even without companion .fmt declaration
        "glob": ["*access.log", "/var/log/apache*/*acc*.log"],
    }

    # date/time strings
    strftime = {
        "class": "strftime",
        "placeholder": "%\w",
        "rewrite": {
            "%[EO_^0#\-]+(\w)": "%$1"   # %E, %O alternative formats, glibc prefix extensions
        },
        "#doc": "https://www.man7.org/linux/man-pages/man3/strftime.3.html",
        "fields": {
            "%a": { "id": "tm_wday", "rx": "\w+" },
            "%A": { "id": "tm_wday", "rx": "\w+" },
            "%b": { "id": "tm_mon", "rx": "\w+" },
            "%B": { "id": "tm_mon", "rx": "\w+" },
            "%c": { "id": "tm_dt", "rx": "[-:/.\w\d]+" },
            "%C": { "id": "tm_cent", "rx": "\d\d" },
            "%d": { "id": "tm_mday", "rx": "\d\d" },
            "%D": { "id": "tm_mdy", "rx": "\d+/\d+/\d+" }, #%m/%d/%y
            "%e": { "id": "tm_mday", "rx": "[\d\s]\d" },
            "%F": { "id": "tm_date", "rx": "\d\d\d\d-\d\d-\d\d" },  # %Y-%m-%d
            "%G": { "id": "tm_wyear", "rx": "\d\d\d\d" },
            "%g": { "id": "tm_wyearnc", "rx": "\d\d" },
            "%h": { "id": "tm_mon", "rx": "\w+" },
            "%H": { "id": "tm_hour", "rx": "\d\d" },
            "%I": { "id": "tm_hour", "rx": "\d\d" },
            "%j": { "id": "tm_yday", "rx": "\d\d\d" },
            "%k": { "id": "tm_hour", "rx": "\d\d" },
            "%l": { "id": "tm_hour", "rx": "[\d\s]\d" },
            "%m": { "id": "tm_mon", "rx": "\d\d" },
            "%M": { "id": "tm_min", "rx": "\d\d" },
            "%n": { "id": "newline", "rx": "\\n" },
            "%p": { "id": "tm_ampm", "rx": "AM|PM" },
            "%P": { "id": "tm_ampm", "rx": "am|pm" },
            "%r": { "id": "tm_time", "rx": "\d\d:\d\d:\d\d [AMPM]{2}" },
            "%R": { "id": "tm_time", "rx": "\d\d:\d\d" },
            "%s": { "id": "tm_epoch", "rx": "\d+" },
            "%S": { "id": "tm_sec", "rx": "\d\d" },
            "%t": { "id": "tab", "rx": "\\t" },
            "%T": { "id": "tm_time", "rx": "\d\d:\d\d:\d\d" },
            "%u": { "id": "tm_wday", "rx": "[1-7]" },
            "%U": { "id": "tm_yday", "rx": "[0-5]\d|5[0123]" },
            "%V": { "id": "tm_yday", "rx": "\d\d" },
            "%w": { "id": "tm_wday", "rx": "[0-6]" },
            "%W": { "id": "tm_yday", "rx": "\d\d" },
            "%x": { "id": "tm_ldate", "rx": "[-./\d]+" },
            "%X": { "id": "tm_ltime", "rx": "[:.\d]+" },
            "%y": { "id": "tm_year", "rx": "\d\d" },
            "%Y": { "id": "tm_year", "rx": "\d\d\d\d" },
            "%z": { "id": "tm_tz", "rx": "[-+]\d\d\d\d" },
            "%Z": { "id": "tm_tz", "rx": "\w+" },
            "%+": { "id": "tm_date", "rx": "[-/:. \w\d]+" },
            "%%": { "id": "percent", "rx": "%" },
        },
        "expand": {
            "%(\w)": "[\w\d.]+"
        }
    }
    
    nginx = {
        "class": "nginx",
        "separator": " ",
        "placeholder": "[$](\w+)",
        "rewrite": {
            "(?<!\\\\)([\[\]\|\(\)])": r"\$1",  # escape any regex meta chars in format string
        },
        "#doc": "http://nginx.org/en/docs/http/ngx_http_core_module.html#var_args",
        "fields": {
            "$request": { "id": "request", "rx": "(?<request_method>\w+) (?<request_path>\S+) (?<request_protocol>[\w/\d.]+)" }, 
            "$remote_addr": { "id": "remote_addr", "rx": "[\da-f.:]+" },
            "$remote_user": { "id": "remote_user", "rx": "[\w\-@.:]+" },
            "$time_local": { "id": "time_local", "rx": "[\d/\w:.+\-]+" },
            "$status": { "id": "status", "rx": "\d+", "type": "int" },
            "$request_length": { "id": "request_length", "rx": "\d+", "type": "int" },
            "$request_time": { "id": "request_time", "rx": "[\d.]+" },
            "$msec": { "id": "msec", "rx": "[\d.]+" },
            "$scheme": { "id": "scheme", "rx": "\w+" },
            "$args": { "id": "args", "rx": "\S*" },
            "$is_args": { "id": "is_args", "rx": "\??" },
            "$body_bytes_sent": { "id": "body_bytes_sent", "rx": "\d+", "type": "int" },
            "$http_referer": { "id": "http_referer", "rx": "\S*" },
            "$http_user_agent": { "id": "http_user_agent", "rx": "\S*" },
            "$pipe": { "id": "pipe", "rx": "[p.]" },
            "$ssl_protocol": { "id": "ssl_protocol", "rx": "[\w.]*" },
            "$ssl_cipher": { "id": "ssl_cipher", "rx": "[\w\-.]*" },
        },
        "expand": {
            "[$](\w+)": { "id": "$1", "rx": "\S*", "grok": "QS" }
        },
    }
    
    inilog = {
        "#note": "this is an alias for the »logfmt« key=value serialization (as rediscovered by Go/Heroku peeps)",
        "class": "inilog",
        "record": "*",
        "fields": {
            "*": { "id": "*", "rx": ".+" }
        },
        "container": {
            "*": {
                "rx": "(\w+)=(?:(\S+)|\"(.*?)\")",
                "id": "$1",
                "value": "$2$3",
                "class": "inilog"
            }
        },
    }
    
    # return builtin definitions or from /usr/share/logfmt/*.*.fmt
    @staticmethod
    def get(cls):
        rules = {}
        cls = cls.split(" ")
        while cls:
            lookup = ".".join(cls)
            lookup_ = "_".join(cls)
            add = {}
            dir = "/usr/share/logfmt"
            if not os.path.exists(dir):  # kludge for Python package
                dir = re.sub("[\w.]$", "share", __file__) # use bundled ./share/ directory
            fn = f"{dir}/{lookup}.fmt"
            if os.path.exists(fn):
                add = open(fn, "r", encoding="utf-8").read()
                add = re.sub("^\s*#.+", "", add, re.M)
                add = json.loads(add)
            #elif *.grok: read, find primary regex:, or declare %GROK per cls=["grok", "-"]
            #elif *.lnav: get readymade "regex:"
            else:
                add = rulesdb.__dict__.get(lookup, {}) or rulesdb.__dict__.get(lookup_, {})
            rulesdb.merge(rules, add)
            cls.pop()
        return rules

    # extend set of rules (recursive dictionary merging, without overwriting previous values)
    @staticmethod
    def merge(rules, add):
        for k,v in add.items():
            if isinstance(v, dict):
                if not k in rules:
                    rules[k] = {}
                rulesdb.merge(rules[k], v)
            elif not k in rules:
                rules[k] = v
        return rules

    # development: create share/*.fmt dumps from builtin definitions
    def extract_all(self):
        for key,val in rulesdb.__dict__.items():
            if isinstance(val, dict):
                open(f"share/{key}.fmt", "w").write(json.dumps(val, indent=4))
#rulesdb().extract_all()


# should be the other way round: regex() is meant to be a subset of update()
def update(fmt):
    fmt["regex"] = regex(fmt, update=True)

# assemble regex for format string
def regex(fmt, update=False):
    """
        Create regex for log fmt{}
        
        Arguments
        ---------
        fmt : dict
            Should contain record and class

        return : string
            Combined regex
    """

    rules = rulesdb.merge(
        fmt,
        rulesdb.get(fmt["class"])
    )
    fields = rules["fields"]
    record = fmt["record"]
    if update:
        for field in ["rewrite", "fields", "expand", "alias", "container"]:
            if not field in fmt:
                fmt[field] = {}

    # pre-cleanup (for irrelevant format string `%!200,500<s` control prefixes)
    if "rewrite" in rules:
        for rx, repl in rules["rewrite"].items():
            record = rx_sub(rx, repl, record)

    # create fields from variant placeholders
    if "expand" in rules:
        rx_quote_alt = { # (is_quoted + rx) can map to alternative regex
            (False,  '[^"]*'):  "\S*",
            (True,   "\S+"):    "(?:[^\"]*|\\\\\")+",
        }
        for rx, expand in rules["expand"].items():
            for is_quoted, match, *uu in re.findall(f"(\"?)({rx})", record):
                if match in fields:
                    continue
                x = copy(expand)
                # id: is usually "$1", but might be "prefix_$2" or something
                if x["id"].find('$') >= 0:
                    x["id"] = rx_sub(rx, x["id"], match)
                    x["id"] = re.sub("\W+", "", x["id"]).lower()
                # recurse into other pattern types
                if not "rx" in x and "class" in x:
                    x["rx"] = regex({
                        "class": x["class"],
                        "record": rx_sub(rx, x.get("record") or "$1", match)
                    })
                # regex alternatives, depending on quotes preceeding the placeholder
                if is_quoted and "if_quoted" in x:  # maybe an `if_quoted` definition makes this block redundant
                    x["rx"] = x["if_quoted"]
                elif (is_quoted, x["rx"]) in rx_quote_alt:
                    x["rx"] = rx_quote_alt[(is_quoted, x["rx"])]
                fields[match] = x
                        
    # catch-all \S+ for completely unknown placeholders
    if "placeholder" in rules:
        for ph in re.findall(rules["placeholder"], record):
            if not ph in fields:
                id = re.sub("\W+", "", ph)
                fields[ph] = { "id": id, "rx": "\S+" }

    # do the actual replacement
    def sub_placeholder(m):
        ph = fields[m.group(0)]
        if update:
            fmt["fields"][m.group(0)] = ph  # store used placeholders in fmt
        rx = ph["rx"]
        id = ph["id"]
        # check for existing (…) capture group to mark up
        if re.search("(?<!\\\\)\((?!\?)", rx):
            rx = re.sub("(?<!\\\\)\((?!\?)", f"(?<{id}>", rx, re.M, 1)
        else:
            rx = f"(?<{id}>{rx})"
        return rx
    rx = re.sub(rules["placeholder"], sub_placeholder, record)
    rx = rename_duplicates(rx)
    return rx

# (?<duplicate2>)
def rename_duplicates(rx):
    fields = []
    def count_ph(m):
        s, i = m.group(1), 1
        while s in fields:
            i += 1
            s = f"{m.group(1)}{i}"
        fields.append(s)
        return s
    return re.sub("(?<=\(\?\<)(\w+)(?=\>)", count_ph, rx)

# (?<name>) to (?P<name>)
def rx2re(rx):
    return re.sub("\(\?<(?=\w+>)", "(?P<", rx)

# allow for $1, $2, $3 in re.sub()
def rx_sub(pattern, replacement, source, flags=0):
    if replacement.find('$') >= 0:
        replacement = re.sub(r'[\\\\](?=[0-9])', '$', replacement)
    return re.sub(pattern, replacement, source, flags)

# replace $0 $1 $2 in string with entries from list
def repl_sub_dict(s, row):
    return re.sub("\$(\d+)", lambda m: row.get(int(m.group(1))), s)


# file-style wrapper that yields parsed dictionaries instead of string lines
class parsy_parse:

    def __init__(self, logfn="", fmt=None, debug=False, fail=False, duplicate=True):
        """
            Open log file and .fmt specifier, to iterate log lines as dictionary.
            Alternatively to *.log.fmt allows to specify fmt={"class":"apache error"}
            or even fixated {"record":"%a %t %e %F"} formatstring.
            Dictionaries should contain both expanded entries and aliases unpacked.
        """
        self.debug = debug
        self.fail = fail
        self.duplicate = duplicate
        # try + nicer error....
        self.f = open(logfn, "r", encoding="utf-8")
        if not fmt:
            try:
                fmt = json.loads(open(f"{logfn}.fmt", "r", encoding="utf-8").read())
            except Exception as e:
                sys.stderr.write(str(e) + "\n")
                sys.stderr.write("Use `update-logfmt` or `modseccfg`→File→Install→update_logfmt.py to generate a *.log.fmt descriptor.\n")
                fmt = {"class":"apache combined"}
                #fmt = rulesdb.find_by_glob(logfn)
        fmt = rulesdb.merge(
            fmt,   # this should be in regex/update
            rulesdb.get(fmt.get("class"))
        )
        self.alias = fmt.get("alias", {})
        self.container = fmt.get("container", {})
        self.rx = re.compile(rx2re(regex(fmt)))

    # allow iterating multiple times?
    def __iter__(self):
        self.f.seek(0, os.SEEK_SET)
        return self

    # iterate over lines, and unpack with regex and aliases
    def __next__(self):
        line = self.f.readline()
        if not line:  # should be implied really
            raise StopIteration()
        m = self.rx.match(line)
        if m:
            d = m.groupdict()
            if self.container:
                self.container_expand(d)
            if self.duplicate:
                for trg,src in self.alias.items():
                    if src in d and not trg in d:
                        d[trg] = d[src]
            return d
        elif self.debug:
            self.debug_rx(line)
            if self.fail:
                raise StopIteration()
        elif self.fail:
            raise StopIteration()
        else:
            pass # just try next line
    
    # pass .close() and similar to file object
    def __getattr__(self, name):
        return getattr(self.f, name)

    # unpack [key "value"] fields
    def container_expand(self, d):
        for k,opt in self.container.items():
            if not k in d:
                continue
            # find `(key)……(val+)` pairs according to regex
            for row in re.findall(opt["rx"], d[k]):
                id = repl_sub_dict(opt.get("id", "$1"), row)
                val = repl_sub_dict(opt.get("val", "$2"), row)
                # pack into list, if key is duplicated
                if not id in d:
                    d[id] = val
                elif not isinstance(d[id], list):
                    d[id] = [d[id], val]
                else:
                    d[id].append(val)

    # get column names (from regex, in order of appearance)
    def names(self):
        return re.findall("\(\?P?<(\w+)>", self.rx.pattern)

    # ANSI output for debugging regex/fmt string
    def debug_rx(self, line):
        rx = self.rx.pattern
        line = line.rstrip()
        #rx_cut = re.compile("[^)]*  \(\?P<\w+>  ( [^()]+ | \([^()]+\) )+  \)  [^()]* \Z", re.X)
        # iteratively strip (?...) capture groups
        while len(rx) and rx.find("(?P<") >= 0:
            #fail = rx_cut.search(rx)
            #if fail: fail = fail.group(0)
            #else: fail = "<unknown-last-capture>"; break
            last = rx.rindex("(?P<")
            if last < 1:
                fail = "<unknown-last-capture>"; break
            fail = rx[last:]
            #print(f"testfail: `{fail}`")
            try:
                rx = rx[0:last]
                rx = re.sub("[^)]*$", "", rx)
                if re.match(rx, line):
                    break # works now, so `fail` was the culprit
            except:
                # likely broke regex nesting, try removing next (?...)
                pass
        try:
            matched = re.match(rx, line)
            matched = matched.group(0)
        except:
            matched = ""
        print("\033[36m" + "failed regex section: \033[1;33;41m" + fail + "\033[40;0m")
        print("\033[42m" + matched + "\033[41m" + line[len(matched):] + "\033[40;0m")

# alias
logopen = parsy_parse

