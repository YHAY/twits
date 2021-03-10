# twits
restful server side flask

1) 회원가입

[POST] 127.0.0.1:5000/users
{
"id":"ccc",
"pw":"123",
"name":"test",
"country":1,
"device_number":"M241A12311"
}

curl -X POST \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  -d '{"id":"aaa", "pw":"123", "name":"test", "country":1, "device_number":"M241A12311"}' \
  "http://127.0.0.1:5000/users"


2) 탈퇴

[DELETE] 127.0.0.1:5000/users
{
"id":"aaa",
"pw":"124&*&a",
"device_number":"M241A12311"
}
-d '{"id":"aaa","pw","123",device_number":"M241A12311"}' \

curl -X DELETE \
-H "Content-type: application/json" \
-H "Accept: application/json" \
-d '{"id":"ccc","pw":"123","name":"test"}' \
"http://127.0.0.1:5000/users"


3) 로그인

[GET] 127.0.0.1:5000/users
{
"id":"aaa",
"pw":"1212121",
"device_number":"M241A1231"
}

curl -X GET \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  -d '{"id":"aaa","pw":"1234","device_number":"M2412"}' \
  "http://127.0.0.1:5000/users"

4) 로그아웃 > 내용이 없음. 추가개발 필요.
5) 회원정보 조회 > 내용이 없음. 추가개발 필요.
6) 회원정보 변경 > 내용이 없음. 추가개발 필요.

7) 사용자매칭

[PUT] 127.0.0.1/game/matching/<user_token>

curl -X PUT \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  "http://127.0.0.1:5000/game/matching/"50dbede3-2cac-44c3-bad4-ab26110c243e""
