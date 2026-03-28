## self-hosted runner 띄우기 kubectl apply -f ~/git/backstage/projects/actions-runner/runner-deployment.yaml -n actions-runner-system


---
## runner 내에서 주소 셋팅
cd 과정에서 문제가 argocd.test.com 주소는 로컬에서만 가능한 주소라서 pod 내에서 접근이 불가하다

```
k exec -it self-hosted-runners-8jw4m-pqn4b -n actions-runner-system -- sh
$ hostname
self-hosted-runners-8jw4m-pqn4b

$ curl argocd.test.com
curl: (7) Failed to connect to argocd.test.com port 80 after 5 ms: Couldn't connect to server
```

해결 방법은 클러스터 내 서비스 주소 쓰기

```
$ curl https://argocd-server.argocd
curl: (60) SSL certificate problem: self-signed certificate
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.

$ curl -k https://argocd-server.argocd
<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>Argo CD</title><base href="/"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" type="image/png" href="assets/favicon/favicon-32x32.png" sizes="32x32"/><link rel="icon" type="image/png" href="assets/favicon/favicon-16x16.png" sizes="16x16"/><link href="assets/fonts.css" rel="stylesheet"><script defer="defer" src="main.8e8aaba661d82e022012.js"></script></head><body><noscript><p>Your browser does not support JavaScript. Please enable JavaScript to view the site. Alternatively, Argo CD can be used with the <a href="https://argoproj.github.io/argo-cd/cli_installation/">Argo CD CLI</a>.</p></noscript><div id="app"></div></body><script defer="defer" src="extensions.js"></script></html>$
```

---
## Docker hub에 ci 이미지 확인
ci에서 일어나는 이미지 build and push 가 정상 수행되었는지 확인

```
curl -s "https://hub.docker.com/v2/repositories/banzzakks/backstage/tags" | jq -r '.results[].name'

python-app-079fffc1e7884d78a96c3da5b82a5ab8d64f0c25
python-app-67740e10f4e235707a8c32b85962a645ef135142
python-app-703ac8acd55911bb5ae5fb0ac57382544eadd5d2
python-app-30956c72a3e99c3cfaf0a6c330e306ff4085c507
python-app-9e6036f93938e858d0b0799e145ededc4e3e53c2
python-app-427fbbc4c79df0186289d39c9ce0a00380dd5fb5
python-app-a8d7fd0ad1f666312da4ea39ee0de763dd1b8feb
python-app-v0.2

```
