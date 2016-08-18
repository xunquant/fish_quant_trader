# encoding: UTF-8

'''
定义所有json字典，每个字典对应一种查询目标
'''

successful_reservation={
	"query" :{
		"filtered":{
			"filter":{
				"bool":{
					"must": {
						"term": {"process_result": "Success"}
					},
					"should":[
						{"term": {"process_original": "Book"}},
						 {"term": {"process_original": "BookNotify"}}
					]
				}
			}
		}
	}
}

failed_reservation={
	"query" :{
		"filtered":{
			"filter":{
				"bool":{
					"must": {
						"term": {"process_result": "Fail"}
					},
					"should":[
						{"term": {"process_original": "Book"}},
						 {"term": {"process_original": "BookNotify"}}
					]
				}
			}
		}
	}
}

cancel_reservation={
	"query" :{
		"filtered":{
			"filter":{
				"bool":{
					"must": {
						"term": {"process_result": "Success"}
					},
					"should":[
						{"term": {"process_original": "Cancel"}},
						 {"term": {"process_original": "CancelNotify"}}
					]
				}
			}
		}
	}
}