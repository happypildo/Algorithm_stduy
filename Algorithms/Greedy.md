# Greedy - 탐욕법
> 가장 좋아보이는 것을 탐욕스럽게 선택해 나가는 기법
> 
- 개념 자체는 크게 어려운 것은 아니지만, 중요하게 생각하는 것은 **greedy로 최적 해를 찾을 수 있냐**가 중요하다.
<br>
<br>

## 예제 문제 - 거스름돈

> 나는 점원이다. 카운터에서 거스름돈으로 사용할 500, 100, 50, 10원 동전이 무한히 존재한다.  <br>
> 손님에게 거슬러 줘야 할 돈이 N원일 때, 거슬러 줘야 할 동전의 최소 개수를 구하라. 단, 여기서 N은 항상 10의 배수이다.

<br>
<br>

## Greedy approach

### Greedy로 풀 수 있을까?

- 가장 좋아보이는 것이 뭘까? 

  → 문제의 정의는 “거스름 돈의 최소 개수”이다.

  → 500원 동전을 먼저 준다면 **최소가 될 수 있을 것 같다**.

| 1260원 | 500원 | 100원 | 50원 | 10원 |
| --- | --- | --- | --- | --- |
| 개수 | 2 | 2 | 1 | 1 |
| 남은 금액 | 1260 - 500*2 = 260 | 260 - 100 * 2 = 60 | 60 - 50 * 1 = 10 | 10 - 10 * 1 = 0 |
| 1260원 | 10원 | 50원 | 100원 | 500원 |
- 간단한 테스트를 해 보아도 뭔가 맞는 것 같다. <br>
  → 이에 따른 java code는 아래와 같다.

<br>

```java
import java.util.Scanner;

public class Solution{
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		
		int T = sc.nextInt();
		
		for(int t_iter = 1; t_iter < T+1; t_iter++) {
			int N = sc.nextInt();
			int[] possible_money = {500, 100, 50, 10};
			
			int cnt = 0;
			for(int i=0; i<possible_money.length; i++) {
				int curr_cnt = (int) N / possible_money[i];
				N = N - curr_cnt * possible_money[i];
				cnt = cnt + curr_cnt;
			}
			
			System.out.println("거스름 돈을 줄 수 있는 동전의 수: " + cnt);
		}
	}
}
```

<br>

### 왜 이게 최적 해일까?

- 풀이를 보고 가장 먼저 생각한 것은 “이런 유형의 문제에 greedy가 항상 적용될 수 있는가?”였다.
    - ChatGPT에게 물어보니 “동전의 단위가 배수 관계일 경우”라고 한다.
    → 위 예제에서 400원이 추가됐다고 해보자.
    
    | 1260 | 500 | 400 | 100 | 50 | 10 |
    | --- | --- | --- | --- | --- | --- |
    | 개수 | 2 | - | 2 | 1 | 1 |
    | 남은 금액 | 260 | 260 | 60 | 10 | 0 |
    | (다른풀이) 개수 | 0 | 3 | 0 | 1 | 1 |
    | (다른풀이) 금액 | 1260 | 60 | 60 | 10 | 0 |
    
    
    - 위 예제에서는 다른 풀이(Dynamic Programming) 방식이 최적이다. 500과 400배 서로 배수 관계가 아니기 때문.
    

    | 1260 | 400 | 100 | 50 | 10 |
    | --- | --- | --- | --- | --- |
    | 개수 | 3 | 0 | 1 | 1 |
    | 금액 | 60 | 60 | 10 | 0 |
    
    - 500이 없을 때는 모두가 배수 관계이기에 만족한다. 경험적으로는 이 것이 맞다고 생각이된다.
    - 그러나 DP가 global optimal은 언제나 만족시켜 줄 수 있기 때문에 개인적으로는 DP 방식을 어떻게 활용하는지 아는 것이 greedy보다 좋다고 생각이 된다.

## 고찰
- 동전들이 "배수" 관계일 때 greedy를 사용할 수 있는 이유는 다음과 같다고 생각한다.
- Greedy가 적용될 수 있는 것은 ***미래를 생각하지 않고 지금의 선택에 최선을 다하면 될 때***이다.
  - 동전이 배수가 된다는 것은, <span style="color:red">어떤 동전을 사용하든 그의 배수가 되는 동전을 사용하는 것이 이득</span>이라는 것이다.
    - <span style="color:red">100원짜리 동전 5개 사용할 것이면, 500원을 쓰는게 이득이다.</span>
  - 동전이 배수가 안 된다는 것은, 내가 지금 사용하는 동전이 이득인지 정확히 모른다는 것이다.
    - 400원짜리 동전을 쓰는 것이 이득인지, 500원을 쓰는 것이 이득인지

<br>
<br>

# 관련 문제 풀이

## BOJ-Greedy-1931
> 회의실 예약 정보(시작 시간, 끝나는 시간)가 주어질 때, 최대한 많이 회의실 예약을 잡고자 한다. <br>
> 회의 시간이 겹치지 않도록 해야 할 때, 최대로 예약할 수 있는 회의 개수는?

### 왜 greedy일까?
- 회의가 끝난 뒤, 다른 회의가 시작될 수 있으므로 <span style="color:red">"현재 예약한 회의 시간 이후"</span>는 **생각하지 않아도 됨**
- 그럼 현재 예약한 회의 시간은 <span style="color:red">"가능한 시간대"</span>에서 **가장 빨리 끝나야 함**
- 그렇기에 **greedy**
> 위 동전 문제와 결이 같다고 볼 수 있다.

### 접근 방법
1. 회의실 예약 시간 중 끝나는 시간을 기준으로 정렬 <br>
	1-1. 여기서, 동일한 끝나는 시간을 갖는다면, **시작하는 시간**을 기준으로 정렬 <br>
	1-2. 예시) (0, 0), (1, 1), (0, 1)이 들어온다면, 정렬되는 순서의 인덱스는 [0 2 1]이 되어야 함 <br>
2. 정렬된 예약 시간을 따라서, 시작 시간이 이전 회의의 끝나는 시간과 같거나 느릴 경우 예약 진행 (if문)
3. 끝

``` python
N = int(input())

S_n = []
E_n = []
for n_iter in range(N):
    s, e = map(int, input().split())
    S_n.append(s)
    E_n.append(e)

meeting_count = 0
sorted_idx_of_E_n = sorted(range(len(E_n)), key=lambda k: (E_n[k], S_n[k]))

previous_end_time = -1
for idx in sorted_idx_of_E_n:
    if S_n[idx] >= previous_end_time:
        meeting_count = meeting_count + 1
        previous_end_time = E_n[idx]

print(meeting_count)
```


## BOJ-Greedy-2217

> N(1 ≤ N ≤ 100,000)개의 로프가 있다. 이 로프를 이용하여 이런 저런 물체를 들어올릴 수 있다. 각각의 로프는 그 굵기나 길이가 다르기 때문에 들 수 있는 물체의 중량이 서로 다를 수도 있다.
> 
> 
> 
> 하지만 여러 개의 로프를 병렬로 연결하면 각각의 로프에 걸리는 중량을 나눌 수 있다. k개의 로프를 사용하여 중량이 w인 물체를 들어올릴 때, 각각의 로프에는 모두 고르게 w/k 만큼의 중량이 걸리게 된다.|
> 
> 각 로프들에 대한 정보가 주어졌을 때, 이 로프들을 이용하여 들어올릴 수 있는 물체의 최대 중량을 구해내는 프로그램을 작성하시오. 모든 로프를 사용해야 할 필요는 없으며, 임의로 몇 개의 로프를 골라서 사용해도 된다.
> 

### 접근법

- 사실 greedy로 어떻게 해야할지 감이 안 왔다.
- 그래서 exhaustive search를 먼저 생각하고, 전체를 볼 필요 없다에 도달했다.

### 풀이

1. 먼저 로프가 견딜 수 있는 힘을 정렬한다.
→ sorted_strength = [a, b, …] (N)
2. 그러면 모든 로프 조합에 대해 견딜 수 있는 하중은 [N * a, (N-1) * b, …] 가 된다.
3. 이 중 최대값을 반환한다.

``` python
N = int(input())

strengths = []
for n_iter in range(N):
    strength = int(input())
    strengths.append(strength)

sorted_strengths = sorted(strengths)
possible_weight = [s * w for s, w in zip(sorted_strengths, range(N, -1, -1))]

print(max(possible_weight))
```

## 큰 수의 법칙 - 책

> 배열의 크기 N, 숫자가 더해지는 횟수 M, 그리고 제약 K가 주어질 때 큰 수의 법칙에 따른 결과를 출력

큰 수의 법칙:
어떠한 수열이 주어졌을 때, 원소들을 M번 더하여 가장 큰 수를 만드는 것이다.
이 때, 동일한 인덱스의 수열 값은 ‘연속적으로’ K번까지만 더해질 수 있다.
따라서, [2, 4, 5, 4, 6] (M=8, K=3)일 때 6 + 6 + 6 + 5 + 6 + 6 + 6 + 5  = 46이 정답이다.
> 

```java
import java.util.Scanner;

public class Solution{
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		
		int N = sc.nextInt();
		int M = sc.nextInt();
		int K = sc.nextInt();
		int[] arr = new int[N];
		
		int first_max_num = -1;
		int first_max_idx = -1;
		
		int second_max_num = -1;
		int second_max_idx = -1;
		
		for(int n=0; n<N; n++) {
			arr[n] = sc.nextInt();
			if(first_max_num < arr[n]) {
				first_max_num = arr[n];
				first_max_idx = n;
			}
		}
		
		for(int n=0; n<N; n++) {
			if(second_max_num < arr[n] && n != first_max_idx) {
				second_max_num = arr[n];
				second_max_idx = n;
			}
		}
		
		int result = (int) (M / (K + 1)) * (K * first_max_num + second_max_num) + (M % (K + 1)) * first_max_num;
		System.out.println(result);
	}
}
```

## 카드 뒤집기 - 책

> N by M 카드 배열이 주어졌을 때, 사용자는 하나의 행을 정할 수 있다. 
이후, 행에서 “가장 작은 수”가 적힌 카드만을 골라야 한다.
여기서, 얻을 수 있는 “가장 큰 수”는 무엇인가?
> 

```java
import java.util.Scanner;

public class Solution{
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		
		int N = sc.nextInt();
		int M = sc.nextInt();
		
		int max_val_in_total = -1;
		
		for(int n=0; n<N; n++) {
			int min_val_in_row = 101;
			
			for(int m=0; m<M; m++) {
				int val = sc.nextInt();
				if(min_val_in_row > val) {
					min_val_in_row = val;
				}
			}
			
			if(max_val_in_total < min_val_in_row) {
				max_val_in_total = min_val_in_row;
			}
		}
		
		System.out.println(max_val_in_total);
	}
}
```

## 1로 만들기 - 책

> 어떤 양수 N (≥ 2)이 주어지고, K (≥2)가 주어진다.
우리는 양수 N을 1로 만들고 싶은데, 이 때 가능한 연산은 두 가지이다.
1. N이 K로 나누어 떨어질 경우, K로 나눌 수 있다.
2. N에서 1을 뺀다.
이 두 연산을 통해 N을 1로 만들기 위한 연산의 최소 횟수는?
> 

```java
import java.util.Scanner;

public class Solution{
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		
		int N = sc.nextInt();
		int K = sc.nextInt();
		
		int cnt = 0;
		while(true) {
			if(N == 1) {
				break;
			} else if(N < K) {
				cnt = cnt + N - 1;
				break;
			}
			if(N % K == 0) {
				N = (int) N / K;
				cnt = cnt + 1;
			} else {
				N = N - N % K;
				cnt = cnt + N % K;
			}
		}
		
		System.out.println(cnt);
	}
}
```

