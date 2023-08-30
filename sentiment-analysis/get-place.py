# 사용자A가 추천 탭 클릭했을 때 유사 사용자가 긍정(1)으로 표기했지만 A는 가보지 않은 장소(핀)찾기
# output(list): [‘userId’, ‘mapId’]

from google.cloud import bigquery
client = bigquery.Client()

table_id = "projectid.route_in.sentimental-analysis"

def get_place(sim_users, target_user):
    # 유사한 유저 1명인 경우 
    if len(sim_users) == 1:
        for i in sim_users:
            sim_users_where = "(" + i + ")"
        print(sim_users_where)
    # 유사한 유저 여러명
    else :
        sim_users_where_temp2 = ""
        for i in sim_users:
            sim_users_where_temp1 = i + ","
            sim_users_where_temp2 = sim_users_where_temp2 + sim_users_where_temp1 
        sim_users_where = "(" + sim_users_where_temp2 + ")"
        sim_users_where = sim_users_where.replace(",)", ")")
        print(sim_users_where)

    # Make an API request.
    query_job = client.query(

        """
        SELECT userId, mapId FROM `{}` 
        WHERE 
            userId IN ({})
            AND userId != {}
            AND score = '1'
        """.format(table_id, sim_users_where, target_user),

        location="asia-northeast3",
        job_config=bigquery.QueryJobConfig(
            labels={"example-label": "example-value"},
            maximum_bytes_billed=1000000
        ),
        job_id_prefix="get_place_",
    ) 
    print(query_job)
    return "Complete def get_place"


ex_sim_users = ['user2', 'user5']
ex_target_user = 'user1'
get_place(ex_sim_users, ex_target_user)
