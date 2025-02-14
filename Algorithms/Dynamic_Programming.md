# 중복되는 연산…

- 컴퓨터가 풀기 어려운 문제 중 하나는
    - 최적의 해를 구하기 위해서 <span style="color:orange">**시간이 많이 필요**</span>하다.
    - 또한, 이를 위해 <span style="color:orange">**메모리 공간을 많이 활용**</span>해야 한다.
- 이를 해결해줄 수 있는 방법 중 하나는 <span style="color:orange">*Dynamic Programming*</span>이다

# 간단한 예시 - 피보나치 수열

![스크린샷 2024-08-27 오전 7.24.22.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/faad244b-bc57-4ada-9bfd-e20cd3691143/bd153d8f-b30a-4059-b0f4-c6e0a9edfbdd/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-08-27_%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB_7.24.22.png)

- 피보나치 수열이라 함은, 이전 두 값을 합쳐 현재 값으로 계산하는 수열을 의미한다.
- 이를 <span style="color:orange">***점화식***</span>으로 표현할 수 있다.
    
    > 점화식이란, 인접한 항들 사이의 관계식을 의미한다.
    > 
    - $a_{n+2}=f(a_{n+1}, a_n)=a_{n+1}+a_n$     $(n>2)$

## 재귀로 표현해 보기

- 앞서 본 것과 같이, 피보나치 수열은 <span style="color:orange">**이전 결과 없이 현재 결과를 계산할 수 없다**</span>.
- 이는 재귀의 특성과도 같다.
    
    > 호출된 함수의 결과가 돌아오기까지 (이전 결과가 계산되기 까지) 현재 결과를 계산하지 않는다.
    > 
    
    ```python
    def fibo(x):
    	if x == 1 or x == 2:
    		return 1
    	return fibo(x - 1) + fibo(x - 2)
    ```
    
- 아주 간단하다. 근데 문제가 있다.
    - 하나의 `x`는 두 개의 함수를 호출한다 (`x-1`, `x-2`).
    - 이에 따라 복잡도는 `O(2^N)`이 된다 (N=30일 경우 약 10억 회 연산).
    - <span style="color:orange">이 문제의 근원은 중복된 연산에 있다</span>.
        
        

## 재귀의 문제점 - 중복된 연산

- 아래 사진은 `fibo(6)`을 호출했을 때, 호출되는 함수들을 그래프로 표현한 것이다.

![스크린샷 2024-08-27 오전 7.30.39.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/faad244b-bc57-4ada-9bfd-e20cd3691143/4ad1d023-399b-4e14-99e5-c00a390776bc/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2024-08-27_%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB_7.30.39.png)

- **중복된 연산이 많음**을 알 수 있다.

# 다이나믹 프로그래밍

- DP는 이러한<span style="color:orange"> **중복된 연산을 피할 수 있는 방법**</span> 중 하나이지만, 다음과 같은 <span style="color:orange">**조건이 필요**</span>하다.
    1. 큰 문제를 작은 문제로 나눌 수 있다.
    2. 작은 문제에서 구한 정답은, 그것을 포함하는 큰 문제에서도 동일하다.

## 피보나치 with DP

1. 큰 문제를 작은 문제로 나눌 수 있는가?
    1. 재귀로 호출 되었듯이, 큰 문제를 작은 문제의 합으로 구할 수 있다.
2. 작은 문제에서 구한 정답은 그것을 포함하는 큰 문제에서도 동일하다.
    1. 점화식에서 보았듯이, `N`을 계산하기 위해서는 `N-1`과 `N-2`에서의 문제 해결 값이 사용된다.

```python
DP = [0] * 100

def fibo(x):
	if x == 1 or x == 2:
		return 1
	
	if DP[x] != 0:
		# 0이 아니라는 것은, 이미 계산된 적이 있음을 의미한다.
		return DP[x]
	
	DP[x] = fibo(x - 1) + fibo(x - 2)
	
	return DP[x]
```

- 재귀적으로 호출되는 것은 동일하지만, `if DP[x] != 0`부분에서 계산된 정보를 참고한다.
    - 이를 <span style="color:orange">Memoization</span>이라고도 한다.

## Top-down & Bottom-up

> DP의 문제 풀이 방향성에 관련하여
> 

### Top-down

- 큰 문제를 해결하기 위해 작은 문제를 호출하는 방식
    - 위 피보나치 풀이가 이에 해당한다.

### Bottom-up

- 작은 문제부터 답을 도출하여 최종 해를 구하는 방식
    - 아래 풀이가 이에 해당한다.
    
    ```python
    DP = [0]
    
    DP[1] = 1
    DP[2] = 2
    n = 99
    
    for i in range(3, n+1):
    	DP[i] = DP[i - 1] + DP[i - 2]
    
    print(DP[i])
    ```