# 분석 보고서

## 분석 대상

https://illustar.net/performance-list  
https://api.illustar.net/v1/concert?row_per_page=10&page=1&keyword=  
https://illustar.net/assets/index-CVFG_XFh.js


## 분석 과정

![](screenshots/화면%20캡처%202025-03-21%20113813.png)
일러스타 페스의 전시 공연 창을 들어가면 위와 같은 HTTP 패킷이 오가는 것을 확인 할 수 있다. concert로 보낸 요청의 응답 결과를 보면 위와 같이 모종의 알고리즘을 통해 bytes로 변환된 값을 받아 이를 가공해 전시 공연 목록을 만들어냈음을 유추할 수 있다.

![](screenshots/화면%20캡처%202025-03-21%20113922.png)
이번에는 `index-CVFG_XFh.js` 파일을 살펴보자. `index-*.js`의 파일은 본 홈페이지를 구성하는 메인 스크립트이며 이 파일 내에는 위 사이트를 구성하는 모든 내용이 기술되어 있을 것이다.

그 중에서도 우리는 `/concert`로 가는 요청을 분석할 것이기에 해당 내용을 키워드로 하여 검색해보자. 이를 수행하면 아래와 같은 내용을 발견할 수 있다.
```js
uqe = async (e, t, n) => (await gt(`/concert?row_per_page=${t}&page=${e}&keyword=${n}`)).data
```
위 내용을 통해 `uqe`로 진입하여 `gt`라는 함수를 통해 `/concert`로 API 요청을 하고 있음을 알 수 있다. `gt` 함수의 구현부는 `gt = `을 키워드로 하여 검색하면 아래와 같이 작성되어 있음을 알 수 있다.
```js
;
Cp.interceptors.response.use(phe, hhe);
const gt = (...e) => Cp.get(...e)
  , Gs = (...e) => Cp.post(...e)
```
`gt` 함수는 `Cp.get`와 동일하다는 것을 알 수 있다. 이 중에 특히나 유심히 볼만한 부분은 `Cp`의 다른 메소드를 호출한 바로 윗 줄이었다.

`Cp.interceptors.response.use`를 통해 `Cp`가 `axios`이었음을 알 수 있었다.
`axios.interceptors.response.use`는 함수를 인자로 받아 응답을 인자로 받은 함수로 넣어 변환시키는 기능을 수행한다.

이를 생각하면 인자로 들어간 `phe`가 곧 응답을 전처리하는 함수가 될 것임을 알 수 있으며 그 내용은 바로 위에 아래와 같이 작성되어 있었다.
```js
const phe = e => {
    if (e.status >= 200 && e.status < 300) {
        if (e.data.a) {
            const t = Object.values(e.data.data)
              , n = new Uint8Array(t)
              , r = che.ungzip(n, {
                to: "string"
            })
              , i = JSON.parse(r);
            return {
                ...e.data,
                data: i
            }
        }
        return e.data
    }
    return Promise.reject(e.data)
}
```
위 코드를 통해 우리는 concert로부터 받은 응답의 data 항목을 다음과 같이 핸들링 할 수 있음을 알 수 있다.
```python
import zlib, json

n = bytes(data.values()) # data = {0: 120, 1: 156, ...}
r = zlib.decompress(n)
i = json.loads(r)
```