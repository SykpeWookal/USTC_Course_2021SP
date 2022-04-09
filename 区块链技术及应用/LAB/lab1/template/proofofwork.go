package main

import (
	"crypto/sha256"
	"math"
	"math/big"
	"math/rand"
	"time"
)

var (
	maxNonce = math.MaxInt64
)

const targetBits = 10

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
	rand.Seed(time.Now().UnixNano())
	nonce := 0
	nonce = rand.Intn(1000000000)
		a := sha256.Sum256(pow.block.Data[0])
	pow.block.Hash = a[:]

	return nonce, pow.block.Hash
}

// Validate validates block's PoW
// implement
func (pow *ProofOfWork) Validate() bool {
	return true
}