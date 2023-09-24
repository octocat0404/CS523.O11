#include <bits/stdc++.h>
#define LB(id) 2*id + 1       // Left branch
#define RB(id) 2*id + 2       // Right branch
using namespace std;

struct node         // Segment Tree node
{
    int val;
    int lazy = 0;
};

int N;              // Number of elements in ARRAY
int*  arr = NULL;
node* ST  = NULL;

// Optional
void InputArr()
{
    cout << "Input the ARRAY: ";
    for (int i = 0; i < N; i++)
        cin >> arr[i];
}

void PrintArr()
{
    for (int i = 0; i < N; i++)
        cout << arr[i] << " ";
    
    cout << endl;
}

void PrintST()
{
    for (int i = 0; i < 2*N - 1; i++)
        cout << ST[i].val << " ";
    
    cout << endl;
}


// Primary Functions
void Build(int id = 0, int l = 0, int r = N-1)
{
    // Leaf nodes
    if (l == r) ST[id].val = arr[l];
    else
    {
        int mid = (l+r) / 2;
        Build(LB(id), l, mid);
        Build(RB(id), mid+1, r);
        ST[id].val = ST[LB(id)].val + ST[RB(id)].val;
    }
}


int  Query(int id, int l, int r, int lq, int rq)                    // lq: l-query, rq: r-query
{
    // [l;r] in [lq;rq]
    if (l >= lq && r <= rq) return ST[id].val;

    // [l;r] not in [lq;rq] -> l < lq && r > rq (!above) and l > rq || r < lq
    if (l > rq || r < lq) return 0;
    
    int mid = (l + r) / 2;
    return Query(LB(id), l, mid, lq, rq) + Query(RB(id), mid+1, r, lq, rq);
}

int  Query(int lq, int rq)                                          // Overload for 2 parameters
{
    return Query(0,0, N-1, lq, rq);
}


void UpdatePoint(int id, int l, int r, int arrid, int diff)         // arrid: array-index
{
    if (l == r)     // Leaf nodes
    {
        arr[arrid] += diff;
        ST[id].val += diff;
    }
    else
    {
        int mid = (l + r) / 2;

        if (l <= arrid && arrid <= mid)     // Left branch
            UpdatePoint(LB(id), l, mid, arrid, diff);
        else                                // Right branch
            UpdatePoint(RB(id), mid+1, r, arrid, diff);

        ST[id].val = ST[LB(id)].val + ST[RB(id)].val;
    }
}

void UpdatePoint(int arrid, int diff)                               // Overload for 2 parameters
{
    UpdatePoint(0, 0, N-1, arrid, diff);
}


void UpdateRange(int id, int l, int r, int lu, int ru, int diff)    // lu: l-update, ru: r-update
{
    if (l > r || l > ru || r < lu)      // Out of range
        return;

    if (l == r)
    {
        arr[l] += diff;
        ST[id].val += diff;
        return;
    }

    int mid = (l+r) / 2;
    UpdateRange(LB(id), l, mid, lu, ru, diff);
    UpdateRange(RB(id), mid+1, r, lu, ru, diff);

    ST[id].val = ST[LB(id)].val + ST[RB(id)].val;
}

void UpdateRange(int lu, int ru, int diff)                          // Overload for 3 parameters
{
    UpdateRange(0, 0, N-1, lu, ru, diff);
}



// Lazy Propagation

void LPUpdateRange(int id, int l, int r, int lu, int ru, int diff)    // lu: l-update, ru: r-update
{
    if (ST[id].lazy != 0)		//Make lazy update
    {
    	ST[id].val += (r-l+1)*ST[id].lazy;
    	
    	if (l == r)			//If node is leaf -> update array
        {
        	arr[l] += ST[id].lazy;
		}
		else				//If node is not leaf -> set lazy for its children
		{
			ST[LB(id)].lazy += ST[id].lazy;
    		ST[RB(id)].lazy += ST[id].lazy;
		}
		
		ST[id].lazy = 0;
	}
	
	if (l > r || l > ru || r < lu)      // Out of range
        return;

    if (lu <= l && r <= ru)		//Fully in range
    {
        ST[id].val += (r-l+1)*diff;
        
		if (l == r)			//If node is leaf -> update array
        {
        	arr[l] += diff;
		}
		else				//If node is not leaf -> set lazy for its children
		{
			ST[LB(id)].lazy += ST[id].lazy;
    		ST[RB(id)].lazy += ST[id].lazy;
		}
        return;
    }

    //Not fully in range
	int mid = (l+r) / 2;
    UpdateRange(LB(id), l, mid, lu, ru, diff);
    UpdateRange(RB(id), mid+1, r, lu, ru, diff);

    ST[id].val = ST[LB(id)].val + ST[RB(id)].val;
}

void LPUpdateRange(int lu, int ru, int diff)                          // Overload for 3 parameters
{
    LPUpdateRange(0, 0, N-1, lu, ru, diff);
}


int  LPQuery(int id, int l, int r, int lq, int rq)                    // lq: l-query, rq: r-query
{
    if (ST[id].lazy != 0)		//Make lazy update
    {
    	ST[id].val += (r-l+1)*ST[id].lazy;
    	
    	if (l == r)			//If node is leaf -> update array
        {
        	arr[l] += ST[id].lazy;
		}
		else				//If node is not leaf -> set lazy for its children
		{
			ST[LB(id)].lazy += ST[id].lazy;
    		ST[RB(id)].lazy += ST[id].lazy;
		}
		
		ST[id].lazy = 0;
	}
	
	// [l;r] in [lq;rq]
    if (l >= lq && r <= rq) return ST[id].val;

    // [l;r] not in [lq;rq] -> l < lq && r > rq (!above) and l > rq || r < lq
    if (r < lq || rq < l) return 0;
    
    int mid = (l + r) / 2;
    return Query(LB(id), l, mid, lq, rq) + Query(RB(id), mid+1, r, lq, rq);
}

int  LPQuery(int lq, int rq)                                          // Overload for 2 parameters
{
    return LPQuery(0,0, N-1, lq, rq);
}



int main()
{
    cout << "Input the number of elements in ARRAY: "; cin >> N;
    // Dynamic Allocation
    arr = new int[N];
    ST  = new node[N * 4];

    // Must include
    InputArr();
    Build();

    // Have fun here
    
    PrintArr();
    PrintST();

    // Free Memory
    delete[] arr;
    delete[] ST;
}