# Backstage 테스트 환경 구성 가이드

Udemy 강의 **"From DevOps to Platform Engineering: Master Backstage & IDPs"** 실습 환경 셋업 가이드입니다.

## 환경 구성 개요

```
Docker 이미지 빌드/push
        ↓
kind 클러스터 생성 (control-plane 1 + worker 1)
        ↓
ingress-nginx 설치
        ↓
python-app Helm 배포
        ↓
ArgoCD Helm 배포
        ↓
/etc/hosts 등록 → 브라우저 접속
```

---

## 사전 요구사항

아래 도구들이 설치되어 있어야 합니다.

```bash
docker --version
kind version
kubectl version
helm version
```

미설치 시:

```bash
brew install kind
brew install kubectl
brew install helm
```

---

## Step 1. Docker 이미지 빌드 및 Push

```bash
cd ~/git/backstage/python-app

# 이미지 빌드
docker build -t python-app:v0.2 .

# Docker Hub 태깅 및 push
docker tag python-app:v0.2 banzzakks/backstage:python-app-v0.2
docker login -u banzzakks
docker push banzzakks/backstage:python-app-v0.2
```

---

## Step 2. kind 클러스터 생성

```bash
cd ~/git/backstage/kubectl

kind create cluster --config=cluster
```

클러스터 확인:

```bash
kubectl cluster-info
kubectl get nodes
# NAME                      STATUS   ROLES
# backstage-control-plane   Ready    control-plane
# backstage-worker          Ready    <none>
```

---

## Step 3. ingress-nginx 설치

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Pod가 Running 상태가 될 때까지 대기:

```bash
watch kubectl get pod -n ingress-nginx
```

---

## Step 4. python-app 배포 (Helm)

```bash
cd ~/git/backstage/python-app/charts/python-app

kubectl create namespace python

helm install python-app -n python .

kubectl get all -n python
```

---

## Step 5. ArgoCD 설치 (Helm)

```bash
cd ~/git/backstage/python-app/charts/argocd

helm repo add argo https://argoproj.github.io/argo-helm

helm upgrade --install argocd argo/argo-cd \
  -n argocd --create-namespace \
  -f values-argo.yaml

kubectl get pod -n argocd
```

초기 admin 패스워드 확인:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

---

## Step 6. /etc/hosts 등록

```bash
sudo vi /etc/hosts
```

아래 내용 추가 (ingress.yaml의 호스트명 기준):

```
127.0.0.1  python-app.local
127.0.0.1  argocd.local
```

브라우저에서 접속:
- python-app: `http://python-app.local`
- ArgoCD: `http://argocd.local`

---

## 클러스터 삭제

테스트 환경을 초기화하려면:

```bash
kind delete cluster
```