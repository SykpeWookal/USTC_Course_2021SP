package main

import (
	// "crypto/sha256"
	"bytes"
	"container/list"
	"crypto/sha256"
)

// MerkleTree represent a Merkle tree
type MerkleTree struct {
	RootNode *MerkleNode
}

// MerkleNode represent a Merkle tree node
type MerkleNode struct {
	Left  *MerkleNode
	Right *MerkleNode
	Data  []byte
}

// NewMerkleTree creates a new Merkle tree from a sequence of data
// implement
func NewMerkleTree(data [][]byte) *MerkleTree {
	len_data := len(data)
	Q := list.New()       //双向链表包
	Q.Init()
	//fmt.Print("1\n")
	for i:=0;i < len_data;i++{
		var temp MerkleNode
		temp.Right = nil
		temp.Left = nil
		a := sha256.Sum256(data[i])
		temp.Data = a[:]//a仅用作类型转换
		Q.PushBack(temp)
	}
	//fmt.Print("2\n")
	if (len_data % 2 == 1) {
		var temp MerkleNode
		temp.Right = nil
		temp.Left = nil
		a := sha256.Sum256(data[len_data-1])
		temp.Data = a[:]//a仅用作类型转换
		Q.PushBack(temp)
	}                    //将原始数据做哈希存入队列

	for Q.Len() != 1{
		len_data = Q.Len() //更新长度
		if len_data % 2 == 1 {
			Q.PushBack(Q.Back().Value.(MerkleNode))
			len_data = Q.Len()
		}
		for i:=1;i<=len_data/2;i++ {//取出两个元素，求父节点，放回队尾
			var father MerkleNode
			op1_temp := Q.Front()
			op1_value := op1_temp.Value.(MerkleNode)
			Q.Remove(op1_temp)
			op2_temp := Q.Front()
			op2_value := op2_temp.Value.(MerkleNode)
			Q.Remove(op2_temp)

			father.Left = &op1_value
			father.Right = &op2_value
			var buffer bytes.Buffer //Buffer是一个实现了读写方法的可变大小的字节缓冲
			buffer.Write(op1_value.Data)
			buffer.Write(op2_value.Data)
			op_1add2 :=buffer.Bytes()  //得到了b1+b2的结果
			a := sha256.Sum256(op_1add2)
			father.Data = a[:]
			Q.PushBack(father)
			//fmt.Println(Q.Len())
		}
	}

	a := Q.Front().Value.(MerkleNode)
	var mTree = MerkleTree{&a}
	return &mTree
	//var node = MerkleNode{nil,nil,data[0]}
	//return &mTree
}

func NewMerkleNode(lnode, rnode *MerkleNode, data []byte) *MerkleNode {
	// leaf node
	var node MerkleNode
	if data != nil {
		SHAvalue := sha256.Sum256(data)
		hash := []byte(SHAvalue[:])
		node = MerkleNode{nil, nil, hash}
	} else { // not leaf node
		concat := append(lnode.Data, rnode.Data...)
		SHAvalue := sha256.Sum256(concat)
		hash := []byte(SHAvalue[:])
		node = MerkleNode{lnode, rnode, hash}
	}
	return &node
}