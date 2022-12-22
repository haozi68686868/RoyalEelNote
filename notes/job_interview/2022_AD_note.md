```c++



// vehicle model

//
// x  -----  x
//      L1


// fa      ra1   ra2
// x ------x --- x
//        L1
        
//            L2        

// 



//
// For the 1d motion of a point, the position s, velocity v, and acceleration // a satisfy the following equations:
d(s)/dt = v
d(v)/dt = a
// (1.) Please rewrite the kinematic equations to the state space form, with 
// states x = [s, v]^T, control input u = [a]

// (2.) To design control alogorithms, we usally convert the system from 
// continuous domain to discrete domain. Please write the discrete system
// with time step ts.

// (3.) How to determine the system is controllable?

// (4.) For a close loop discrete system x[k+1]=A*x[k] + B*u[k], 
// with control law u[k] = -Kx[k], how to determine the system is stable?

dx = Ax + Bu

dx = [v a]^T

A= [0 1;0 0]  B= [0 1]^T



s[k+1] = s[k] + v*ts
v[k+1] = v[k] + a*ts

x[k+1]=A*x[k] + B*u[k]
A= [0 ts;0 0] B= [0 ts]^T

rank P = 2 ; P= [B AB]

x[k+1] = (A-BK)x[k]

lambda(sI-A+BK) 的特征值，都是实部<0


// Coding
// 描述: 给定一个 n * m 的迷宫，迷宫中的点为 0(可走）和 1（不可走）。给定 s 和 t，假定每一步距离都为 1，问起点到终点的最短距离。
  
#include <queue>
struct AStarNode
{
    int getHeuristic(Point p,Point t)
    {
      	return std::abs(p.x-t.x)+std::abs(p.y-t.y);
    }
  	int f;
  	int g;
  	int h;
  	Point p_;
  
  	AStarNode(Point cur,Point target,int CurCost)
    {
      	h = getHeuristic(cur,target);
      	g = CurCost;
      	f = g+h;
      	p_ = cur;
    }
  
  	bool operator< (const AStarNode& node) const
    {
      	return f>node.f;
    }
  
};

int solve(const std::vector<std::vector<bool>> map, Point s, Point t)
{
  	std::priority_queue<AStarNode> queue;
  	AStarNode start(s,t,0);
  	queue.emplace_back(start);
  	int dx[4] = {0,0,-1,1};
  	int dy[4] = {1,-1,0,0};
  
  	std::vector<std::vector<bool>> visited;
  	visited.resize(map.size(),vector<bool>(map.front().size(),false);
    visited[s.x][s.y] = true;
    
    const auto checkValid = [&] (const Point& p)->bool
    {
      	return (p.x>=0 && p.y >=0 && p.x < map.size() && p.y < map.front().size()) && !map[p.x][p.y];
    };
  
  	while(!queue.empty())
    {
      	const AStarNode cur = queue.top();
      	queue.pop();
      
      	if(cur.p_ == t)
        {
          return cur.g;
        }
      	for(int i=0;i<4;i++)
        {
          	Point tmp = cur._p;
          	tmp.x +=dx[i];
          	tmp.y +=dy[i];
          	
          	if(checkValid(tmp) && !visited[tmp.x][tmp.y])
            {
              	queue.emplace(tmp,t,cur.g+1);
              	visited[tmp.x][tmp.y] = true;
            }
        }
    }
  
  	return -1;
}
 

```



```c++
DJI

|   |====|   |
----     ——

class Bucket {

public:
  void addWater(double amount)
  {
  		if(parent==nullptr)
      {
      		this->amount_+=amount;
      }
      findRoot()->addWater(amount);
  }
  double getAmount() const
  {
  		if(parent==nullptr)
      {
      		return amount_/(child_cnt+1);
      }
  		return findRoot()->getAmount();
  }
  void link(Bucket* other)
  {
  		if(other==nullptr)
      {
      		return;
		}
      

​```
  Bucket* other_root = other->findRoot();
  other_root->parent = this;
  amount_ += other->amount_;
  this->child_cnt += (other_root->child_cnt+1);
​```

  }

  Bucket* findRoot() const
  {
  		if(parent==nullptr)
      {
      		return this;
      }
  		Bucket* node = parent;
  		while(node->parent!=nullptr)
      {
      		node = node->parent;
      }
      return node;
  }
  mutable double amount_;
  Bucket* parent = nullptr;
  int child_cnt = 0;
};
```



```c++
// 在线面试平台。将链接分享给你的朋友以加入相同的房间。
// Author: tdzl2003<dengyun@meideng.net>
// QQ-Group: 839088532


// 输入N个点（x,y),2D平面
// 输出一个三角形3*(x,y)，这三个点在原始的N个点之中选取
// 要求：剩下的点，都在三角形之外

// N >=100

// 严格在之外

// 

struct Point
{
  	double x;
  	double y;
};

vector<Point> solve(const vector<Point>& pts)
{
  	Point first = pts[0];
  	Point second = pts[1];
  
  	const auto getAngle = [&](Point pt)->double
    {
      	Point vec = pt - first;
      	double angle = std::atan2(vec.x,vec.y);
      	if(angle<0)
        {
          	angle+= (M_PI*2);
        }
      	return angle;
    };
  
  	double selected_angle = getAngle(second);
  	const auto getSide = [&](Point pt)->int
    {
      	double angle = getAngle(pt);
      	
      	if(std::abs(selected_angle-angle)<1e-9)
        {
          	return 0;
        }

        return angle<selected_angle ? -1 : 1;
    };
  
  	
  
  	std::vector<int> sideIdxes;
  	std::vector<int> centerIdxes;
  	
  	for(int i=2;i<pts.size();i++)
    {
      	int side = getSide(pts[i])
        if(side==0)
        {
          	centerIdxes.push_back(i);
        }
      	else
        {
          	sideIdxes.push_back(i);
        }
    }
  	
  	if(!centerIdxes.empty())
    {
      	double minDistance = (second - first).norm();
      	/* const auto compare1 = [&](int idx_a,int idx_b)->bool
        {
          	if(points[idx_a].x==points[idx_b].x)
            {
              	return points[idx_a].y < points[idx_b].y;
            }
          	return points[idx_a].x<points[idx_b].x;
        }; */
      	// oneSideQuickSort(centerIdxes,0,centerIdxes.size()-1, compare1, false);
      	
      	for(int i=0;i<centerIdxes.size();i++)
        {
          	const Point& tmp_pt = pts[centerIdxes[i]];
          	double distance = ( tmp_pt - first).norm();
          	if(distance<minDistance)
            {
              	minDistance = distance;
              	second = tmp_pt;
            }
        }
    }
  	Point third;
  	if(!sideIdxes.empty())
    {
      	double min_angle_error = 100;
      	for(int i=0;i<sideIdxes.size();i++)
        {
          	const Point& tmp_pt = pts[sideIdxes[i]];
          	double angle = getAngle(tmp_pt);
          	double angle_error = std::abs(angle - selected_angle);
          	if(angle_error<min_angle_error)
            {
              	min_angle_error = angle_error;
              	third = tmp_pt;
            }
        }
    }
  	std::vector<Point> res;
  	res.emplace_back(first);
  	res.emplace_back(second);
  	res.emplace_back(third);
  	return res;
  	
}

void oneSideQuickSort(std::vector<int>& idxes,int lo, int hi, std::function<int,int>()/*tbd*/ compare_func, bool direction)
{
  	int selected_idx = lo;
  	int end = hi;
  	int start = lo;
  	lo++;
  	while(true)
    {
      	while(hi>lo &&  compare_func(idxes[selected_idx], idxes[lo])) lo++;
      	while(hi>lo && !compare_func(idxes[selected_idx], idxes[hi])) hi--;
      	if(lo>=hi)
        {
          	break;
        }
      	std::swap(idxes[lo],idxes[hi]);
    }
  	std::swap(idxes[selected_idx],idxes[hi]);
  	if(direction)
    {
      	oneSideQuickSort(idxes,start,hi-1,direction);
    }
  	else
    {
      	oneSideQuickSort(idxes,hi+1,end,direction);
    }
  	
}
```



```c++
class Test02
{
  public:
      template<typename T>
      virtual void function01(T param) {
        //...
      }
};


struct Node {
  int val;
  Node* next = nullptr;
  Node* random_next = nullptr;
  
  Node (int value) : val(value){}
}


Node* copy(Node* root) {
  if(root==nullptr)
  {
      return nullptr;
  }
  // 1. insert mirror node
  Node* cur = root;
  while(cur!=nullptr)
  {
      Node* inserted = new Node(cur->val);
      inserted->next = cur->next;
      cur->next = inserted;
      cur = inserted->next;
  }
  
  // 2. modify mirror node
  cur = root;
  while(cur!=nullptr)
  {
      Node* mirror_node = cur->next;
      if(cur->random_next!=nullptr)
      {
          mirror_node->random_next = cur->random_next->next;
      }
      cur = cur->next->next;
  }
  
  // 3. split
  cur = root;
  Node* res = root->next;
  Node* copied = res;
  cur->next = cur->next->next;
  cur = cur->next;
  while(cur!=nullptr)
  {
      Node* mirror_node = cur->next;
      copied->next = mirror_node;
      copied = copied->next;
      cur->next = cur->next->next;
      cur = cur->next;
  }
  return res;
}
```



```c++
std::vector<int> arg_sort(const std::vector<int>& array) {
    vector<int> indexes;
    indexes.resize(array.size());
    for(int i=0;i<array.size();i++)
    {
        indexes[i]=i;
    }
    const auto compare = [&](int i,int j)->bool
    {
        return array[i]<array[j];
    };
    std::sort(indexes.begin(),indexes.end(),compare);
    return indexes;
}
```



```c++
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int solve(int size,const std::vector<std::vector<int>>& graph)
{
    std::vector<int> parent;
    int res = size-1;
    parent.resize(size);
    for(int i=0;i<size;i++)
    {
        parent[i] = i;
    }
  
    const auto findRoot = [&](int i)
    {
        int root = i;
        int node = i;
        while(parent[root]!=root)
        {
            root = parent[root];
        }
        while(parent[node]!=node)
        {
            int tmp = parent[node];
            parent[node] = root;
            node = tmp;
        }
        return root;
    };
  
    for(const auto& edge : graph)
    {
        int i_root = findRoot(edge[0]);
        int j_root = findRoot(edge[1]);
        if(i_root!=j_root)
        {
            parent[i_root] = j_root;
            res--;
        }
    }
    return res;
}

int main()
{
  int size = 5;
  vector<vector<int>> graph;
  graph.resize(4);
  graph[0].assign({0, 1});
  graph[1].assign({0, 1});
  graph[2].assign({0, 1});
  graph[3].assign({0, 1});
  cout << solve(size,graph) << endl;
  return 0;
}

```



```
// 你必须定义一个 `main()` 函数入口。
#include <iostream>
#include <string>
#include <queue>
#include <set>
using namespace std;


/**

1.   4.    10
5.   8.    12
6.   9.    14

Find the kth smallest number from a row/column sorted array
*/

struct Point
{
    int x_;
    int y_;
    int val_;
    bool operator < (const Point& p) const
    {
        return this->val_ > p.val_;
    }
    Point(int x,int y,int val): x_(x) , y_(y), val_(val)
    {
    }
};

int solve(const vector<vector<int>>& matrix, int kth)
{
    std::priority_queue<Point> queue;
    std::set<std::pair<int,int>> visited;
    queue.emplace(0,0,matrix[0][0]);
    int cnt = 1;
    const auto checkValid = [&](int x,int y)->bool
    {
        return x<matrix.size() && y < matrix.front().size();
    };
    
    while(cnt<kth)
    {
        const Point p = queue.top();
        queue.pop();
        cnt++;
      
        int x = p.x_+1;
        int y = p.y_;
        if(checkValid(x,y))
        {
            Point down_p = Point(x,y,matrix[x][y]);
            if(!visited.count(std::make_pair(x,y))>0)
            {
                queue.push(down_p);
                visited.insert(std::make_pair(x,y));
                
            }
        }
        x = p.x_ ;
        y = p.y_ + 1; 
        if(checkValid(x,y))
        {
            Point right_p = Point(x,y,matrix[x][y]);
            if(!visited.count(std::make_pair(x,y))>0)
            {
                queue.push(right_p);
                visited.insert(std::make_pair(x,y));
            }
        }
    }
    return queue.top().val_;
}

int main()
{
    vector<vector<int>> matrix;
    matrix.resize(3);
    for(int i=0;i<3;i++)
    { 
        for(int j=0;j<3;j++)
        {
            matrix[i].emplace_back(i*3+j+1);
        }
    }
    for(int i=0;i<9;i++)
    {
        std::cout << solve(matrix,i+1) << std::endl;
    }
    return 0;
}
```



```
// 你必须定义一个 `main()` 函数入口。
#include <iostream>
#include <string>
using namespace std;

int main()
{
  cout << "Hello, World!" << endl;
  return 0;
}


class A
{
    process()
    {
      displayVal(); 
    }
public:
    A* instance()
    {
        static A a;
        return &a;
    }
    A& instance()
    {
        static A a;
        return a;
    }
  

  
private:
    A() = default;
    int val;
  
protected:
    setVal(int val);
  
    int getVal(){return val;}
  
    
    
};

class AbstractFactory
{
    virtual A* makeProductA() = 0;
    virtual B* makeProductB() = 0;
};

class WindowsA : public A
{
    
};


class WindowUIFactory : public AbstractFactory
{
    property
    A* makeProductA() {return new WindowA();
          windowA->setStyle();
      }
    B* makeProductA() {return new WindowB(property);}
};

4+7 = 9
  
time  4 7 

 4    4 4
 7    1 7
 10   4 4
 13   1 7 

  time area times average 每人每天
  
  app 上传 平均每天的游戏数；统计天数
  
  6;3
  
  country 平均games;人数；天数
  
  distinct 平均games;人数；天数
  
  distinctId name countryId 平均games;人数；天数
  
  city 平均games;人数；天数
  
  city cityName distinctId 平均games;人数；天数
  
  key 
  
  UserId cityId 平均每天的游戏数；统计天数
  
  statictics average, days
  
  new_average = average*[days/(days+1)] + current_day / (days+1)
```

