package main

import (
	"bytes"
	"container/list"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestNewMerkleNode(t *testing.T) {
	data := [][]byte{
		[]byte("node1"),
		[]byte("node2"),
		[]byte("node3"),
	}

	// Level 1

	n1 := NewMerkleNode(nil, nil, data[0])
	n2 := NewMerkleNode(nil, nil, data[1])
	n3 := NewMerkleNode(nil, nil, data[2])
	n4 := NewMerkleNode(nil, nil, data[2])

	// Level 2
	n5 := NewMerkleNode(n1, n2, nil)
	n6 := NewMerkleNode(n3, n4, nil)

	// Level 3
	n7 := NewMerkleNode(n5, n6, nil)

	assert.Equal(
		t,
		"64b04b718d8b7c5b6fd17f7ec221945c034cfce3be4118da33244966150c4bd4",
		hex.EncodeToString(n5.Data),
		"Level 1 hash 1 is correct",
	)
	assert.Equal(
		t,
		"08bd0d1426f87a78bfc2f0b13eccdf6f5b58dac6b37a7b9441c1a2fab415d76c",
		hex.EncodeToString(n6.Data),
		"Level 1 hash 2 is correct",
	)
	assert.Equal(
		t,
		"4e3e44e55926330ab6c31892f980f8bfd1a6e910ff1ebc3f778211377f35227e",
		hex.EncodeToString(n7.Data),
		"Root hash is correct",
	)
}

func TestNewMerkleTree(t *testing.T) {
	data := [][]byte{
		[]byte("node1"),
		[]byte("node2"),
		[]byte("node3"),
	}
	// Level 1
	n1 := NewMerkleNode(nil, nil, data[0])
	n2 := NewMerkleNode(nil, nil, data[1])
	n3 := NewMerkleNode(nil, nil, data[2])
	n4 := NewMerkleNode(nil, nil, data[2])

	// Level 2
	n5 := NewMerkleNode(n1, n2, nil)
	n6 := NewMerkleNode(n3, n4, nil)

	// Level 3
	n7 := NewMerkleNode(n5, n6, nil)

	rootHash := fmt.Sprintf("%x", n7.Data)
	mTree := NewMerkleTree(data)

	assert.Equal(t, rootHash, fmt.Sprintf("%x", mTree.RootNode.Data), "Merkle tree root hash is correct")
}





type SPVnode struct{
	hash           []byte
	left_or_right  bool   //左侧true 右侧 false
}

func TestSPV(t *testing.T) {
	data := [][]byte{
		[]byte("node1"),
		[]byte("node2"),
		[]byte("node3"),
	}

	var hash1 []byte
	var hash3 []byte
	var hash3_3 []byte

	mTree := NewMerkleTree(data)

		a1 := sha256.Sum256(data[0])
	hash1 = a1[:]
		a3 := sha256.Sum256(data[2])
	hash3 = a3[:]
	var buffer bytes.Buffer //Buffer是一个实现了读写方法的可变大小的字节缓冲
	buffer.Write(hash3)
	buffer.Write(hash3)
	op_2add1 :=buffer.Bytes()  //得到了op2+op1的结果
	a := sha256.Sum256(op_2add1)
	hash3_3 = a[:]
	testdata := []SPVnode{   //校验交易2，给出信息交易1的哈希，以及交易3交易3哈希和的哈希
		SPVnode{
			hash1,
			true,
		}, //node1 hash
		SPVnode{
			hash3_3,
			false,
		},
	}

		a2 := sha256.Sum256(data[1])
	hash_to_check := a2[:]
	SPVroot := SPVCheck(testdata,hash_to_check)
	assert.Equal(t, mTree.RootNode.Data, SPVroot , "Not EXISTS")

}

func SPVCheck(data []SPVnode,hash_to_check []byte)  []byte{
	len_data := len(data)
	Q := list.New()       //双向链表包
	Q.Init()

	temp := SPVnode{
		hash_to_check,
		true, //任意值均可，待检验节点
	}

	Q.PushBack(temp)//先把带校验数据放入

	for i:=0;i < len_data;i++{
		Q.PushBack(data[i])
	}

	for Q.Len() != 1{
		var father SPVnode
		father.left_or_right = true//任意值
			//fmt.Println(Q.Len())
		op1_temp := Q.Front()
		op1_value := op1_temp.Value.(SPVnode)
		Q.Remove(op1_temp)
		op2_temp := Q.Front()
		op2_value := op2_temp.Value.(SPVnode)
		Q.Remove(op2_temp)

		if(op2_value.left_or_right == true){
				//fmt.Println("left")
			var buffer bytes.Buffer //Buffer是一个实现了读写方法的可变大小的字节缓冲
			buffer.Write(op2_value.hash)
			buffer.Write(op1_value.hash)
			op_2add1 :=buffer.Bytes()  //得到了op2+op1的结果
			a := sha256.Sum256(op_2add1)
			father.hash = a[:]
			Q.PushFront(father)

		} else{
				//fmt.Println("right")
			var buffer bytes.Buffer //Buffer是一个实现了读写方法的可变大小的字节缓冲
			buffer.Write(op1_value.hash)
			buffer.Write(op2_value.hash)
			op_1add2 :=buffer.Bytes()  //得到了op1+op2的结果
			a := sha256.Sum256(op_1add2)
			father.hash = a[:]
			Q.PushFront(father)
		}
	}

	return Q.Front().Value.(SPVnode).hash
	/*if bytes.Equal(rootvalue.Data,Q.Front().Value.(SPVnode).hash) == true  {
		return true
	} else{
		return false
	}*/

}