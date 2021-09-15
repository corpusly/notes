

GET /test/_search
{
  "query": {
    "match_phrase": {"kp":"have/dobj_VERB_NOUN"}
  }
}

GET /test/_search
{
  "query": {
    "match_phrase_prefix": {"kp":"PRON/"}
  }
}
