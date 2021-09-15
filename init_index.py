import json,fire
from elasticsearch import Elasticsearch

es = Elasticsearch(['penly.cn'])
config = {
    "settings" : {
		"refresh_interval": "1s",
        "number_of_shards": "3",
		"max_result_window":"2147483647",
		"index.mapping.ignore_malformed": "true",
        "analysis": {
          "filter": {
            "postag_filter": {
              "type": "pattern_capture",
              "preserve_original": "false",
              "patterns": [
                "(^([^_]+)_[a-z]+[,\\.$]?)",
                "(_[a-z\\-\\.\\'\\$0-9]+)$",
                "(_[a-z\\-\\.\\'\\$]+)",
                "(_[^\\w]+)_",
                "([^\\w])_"
              ]
            },
            "postag_filter2": {
              "type": "word_delimiter",
              "type_table": [
                "^ => ALPHA",
                ", => ALPHA",
                "$ => ALPHA",
                "_ => ALPHA",
                ". => ALPHA",
                "- => ALPHA",
                "! => ALPHA",
                "? => ALPHA",
                "' => ALPHA",
                "0 => ALPHA",
                "1 => ALPHA",
                "2 => ALPHA",
                "3 => ALPHA",
                "4 => ALPHA",
                "5 => ALPHA",
                "6 => ALPHA",
                "7 => ALPHA",
                "8 => ALPHA",
                "9 => ALPHA"
              ]
            },
            "unique_filter": {
              "type": "unique",
              "only_on_same_position": "true"
            }
          },
          "analyzer": {
            "postag_ana": {"filter": ["lowercase","postag_filter", "postag_filter2", "unique_filter"], "type": "custom", "tokenizer": "whitespace" },
			"path_ana": {"type": "custom", "tokenizer": "path-tokenizer"},
			"feedback_ana": {"type": "custom", "tokenizer": "feedback-tokenizer"},
            "kp_ana": { "filter": ["lowercase"], "type": "custom", "tokenizer": "keyword"}
          },
		  "tokenizer": {
			"path-tokenizer": { "type": "path_hierarchy",  "delimiter": "/" },
			"feedback-tokenizer": { "type": "path_hierarchy",  "delimiter": "." }
			}
        },
        "number_of_replicas": "0"
    },
    "mappings" : {
		"_source": {"excludes": ["md5"]},
        "properties": {
		 "@timestamp":{"format":"strict_date_optional_time||epoch_millis", "type":"date"},
        "np": { "type": "text", "analyzer": "postag_ana"  },
		"errs": { "type": "text", "analyzer": "path_ana" ,"fielddata":"true" },
		"feedback": { "type": "text", "analyzer": "feedback_ana" ,"fielddata":"true" },
		"kps": { "type": "text", "analyzer": "whitespace" ,"fielddata":"true" },
		"kp": { "type": "text", "analyzer": "postag_ana" ,"fielddata":"true" },
        "postag": { "type": "text", "analyzer": "postag_ana","fielddata":"true"},
		"ske": { "type": "text", "analyzer": "postag_ana","fielddata":"true"},
		"i": { "type": "integer"},
		"score": { "type": "float"},
        "sid": { "type": "keyword"},
		"rid": { "type": "keyword"},
		"uid": { "type": "keyword"},
		"eid": { "type": "keyword"},
		"lem": { "type": "keyword"},
		"lex": { "type": "keyword"},
		"pos": { "type": "keyword"},
		"tag": { "type": "keyword"},
		"head": { "type": "keyword"},
		"chunk": { "type": "keyword"},
		"type": { "type": "keyword"},
		"rel": { "type": "keyword"},
		"gov": { "type": "keyword"},
		"dep": { "type": "keyword"},
		"vp": { "type": "keyword"},
		"ap": { "type": "keyword"},
		"dp": { "type": "keyword"},
		"doc": { "type": "keyword", "index": "false" ,"store": "false"}, # dim arr of dsk
		"info": { "type": "keyword", "index": "false" ,"store": "false"},
		"kw": { "type": "keyword", "index": "false" ,"store": "false", "ignore_above": 60},
		"meta": { "type": "keyword", "index": "false" ,"store": "false"},
        "tc": {"type": "integer" , "index": "false"},
		"sc": {"type": "integer" , "index": "false"},
		"md5": { "type": "text", "store": "false", "norms":"false"},
		"toks": { "type": "keyword", "index": "false" ,"store": "false"},
		"snts": { "type": "keyword", "index": "false" ,"store": "false"},
		"blob": { "type": "binary", "store": "false"},
		"zlib": { "type": "binary", "store": "false"},
		"kps": { "type": "text", "analyzer": "standard","fielddata":"true"},
        "snt": { "type": "text", "analyzer": "standard","fielddata":"true"}
      }
    }
}

def init_index(idxname):
	try:
		if es.indices.exists(idxname):
			print("already exists", idxname)
			es.indices.delete(idxname)
		es.indices.create(idxname, config) #, body=snt_mapping
	except Exception as e:
		print("exception,", str(e))
	print(">>finished " + idxname )

if __name__ == '__main__':
	fire.Fire(init_index)