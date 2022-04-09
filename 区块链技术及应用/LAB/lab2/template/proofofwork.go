package main

import (
	"bytes"
	"crypto/sha256"
	"math"
	"math/big"
)

var (
	maxNonce = math.MaxInt64
)

const targetBits = 24

// ProofOfWork represents a proof-of-work
type ProofOfWork struct {
	block  *Block
	target *big.Int
}

// NewProofOfWork builds and returns a ProofOfWork
func NewProofOfWork(b *Block) *ProofOfWork {
	target := big.NewInt(1)
	target.Lsh(target, uint(256-targetBits))

	pow := &ProofOfWork{b, target}

	return pow
}


// Run performs a proof-of-work
// implement
func (pow *ProofOfWork) Run() (int, []byte) {
	nonce := 0

	var buf bytes.Buffer
		buf.Write(pow.block.PrevBlockHash)
		buf.Write(pow.block.HashData())
		buf.Write(Int64ToHex(pow.block.Timestamp))
		buf.Write(Int64ToHex(targetBits))
	  tempsum := buf.Bytes()//将上述每次不改变的值的连接用变量记录
	for {
		buf.Reset()
		buf.Write(tempsum)
		buf.Write(Int64ToHex(int64(nonce)))
		hash := sha256.Sum256(buf.Bytes())
		//计算出了哈希值，将其与设定的目标值相比较即可
			tempcmp := new(big.Int)//大数运算包，利用比较函数比较目标值与运算出的哈希值
			tempcmp.SetBytes(hash[:])
		if(tempcmp.Cmp(pow.target) == -1){ //满足条件，直接输出
			pow.block.Hash = hash[:]
			break;
		} else {
			if(nonce < maxNonce){
				nonce = nonce + 1
			} else{ //一直未找到,需要在生成块函数中重新生成时间戳和交易信息，再运行工作量证明
				nonce = -1
				return nonce, hash[:]
			}
		}
	}
	return nonce, pow.block.Hash
}

// Validate validates block's PoW
// implement
func (pow *ProofOfWork) Validate() bool {
	var buf bytes.Buffer
	buf.Write(pow.block.PrevBlockHash)
	buf.Write(pow.block.HashData())
	buf.Write(Int64ToHex(pow.block.Timestamp))
	buf.Write(Int64ToHex(targetBits))
	buf.Write(Int64ToHex(int64(pow.block.Nonce)))

	hash := sha256.Sum256(buf.Bytes())
	hash_bigint := new(big.Int)
	hash_bigint.SetBytes(hash[:])
	if(hash_bigint.Cmp(pow.target) == -1) { //满足条件，直接输出
		return true
	} else {
		return false
	}
}