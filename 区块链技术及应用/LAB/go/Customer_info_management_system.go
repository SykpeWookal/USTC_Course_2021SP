/*
SPDX-License-Identifier: Apache-2.0
*/

package main

import (
	"encoding/json"
	"fmt"
	"strconv"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing
type SmartContract struct {
	contractapi.Contract
}

//定义客户结构体
type Customer struct {
	Age     string `json:"age"`
	Name    string `json:"name"`
	Address string `json:"address"`
	Phone   string `json:"phone"`
}

// QueryResult structure used for handling result of query
type QueryResult struct {
	Key    string `json:"Key"`
	Record *Customer
}

//初始化数据库
func (s *SmartContract) InitDataBase(ctx contractapi.TransactionContextInterface) error {
	customerinfo := []Customer{
		Customer{Age: "31", Name: "Pedc", Address: "Beijing", Phone: "13811111111"},
		Customer{Age: "32", Name: "Mustng", Address: "Shanghai", Phone: "13822222222"},
		Customer{Age: "33", Name: "Tucsow", Address: "HongKong", Phone: "13833333333"},
		Customer{Age: "34", Name: "Passat", Address: "Tokoy", Phone: "13844444444"},
		Customer{Age: "35", Name: "Nacsg", Address: "NewYork", Phone: "13855555555"},
		Customer{Age: "36", Name: "Magtd", Address: "London", Phone: "13866666666"},
		Customer{Age: "37", Name: "Sysrea", Address: "Berlin", Phone: "13877777777"},
		Customer{Age: "38", Name: "Pantodo", Address: "Paris", Phone: "13888888888"},
		Customer{Age: "39", Name: "Nanoro", Address: "Moscow", Phone: "13899999999"},
		Customer{Age: "40", Name: "Bary", Address: "Sydney", Phone: "13812345678"},
	}

	for i, customer := range customerinfo {
		cusinfo_to_byte, _ := json.Marshal(customer) //将信息转化为byte，写入数据库
		err := ctx.GetStub().PutState("C"+strconv.Itoa(i), cusinfo_to_byte)

		if err != nil {
			return fmt.Errorf("Failed to put to world state. %s", err.Error())
		}
	}
	return nil
}

// NewCustomer adds a new customer to the world state with given details
func (s *SmartContract) NewCustomer(ctx contractapi.TransactionContextInterface, Key string, age string, name string, addr string, phone string) error {
	newCustomer := Customer{
		Age:     age,
		Name:    name,
		Address: addr,
		Phone:   phone,
	}

	newCustomer_to_Bytes, _ := json.Marshal(newCustomer) //转化为Byte插入数据库

	return ctx.GetStub().PutState(Key, newCustomer_to_Bytes) //Key主键值
}

// SearchCusInfo returns the customer stored in the world state with given id
func (s *SmartContract) SearchCusInfo(ctx contractapi.TransactionContextInterface, cusKey string) (*Customer, error) {
	cus_bytes, err := ctx.GetStub().GetState(cusKey)

	if err != nil {
		return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
	}

	if cus_bytes == nil {
		return nil, fmt.Errorf("%s does not exist", cusKey)
	}

	customer := new(Customer)
	_ = json.Unmarshal(cus_bytes, customer) //转化为结构体

	return customer, nil
}

// ShowAllInfo returns all info found in world state
func (s *SmartContract) ShowAllInfo(ctx contractapi.TransactionContextInterface) ([]QueryResult, error) {
	startKey := ""
	endKey := ""

	resultsIterator, err := ctx.GetStub().GetStateByRange(startKey, endKey)

	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	results := []QueryResult{}

	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()

		if err != nil {
			return nil, err
		}

		customer := new(Customer)
		_ = json.Unmarshal(queryResponse.Value, customer)

		queryResult := QueryResult{Key: queryResponse.Key, Record: customer}
		results = append(results, queryResult)
	}

	return results, nil
}

// ModifyPhone updates the phone field of customer with given id in world state
func (s *SmartContract) ModifyPhone(ctx contractapi.TransactionContextInterface, cusKey string, newPhone string) error {
	customer, err := s.SearchCusInfo(ctx, cusKey)

	if err != nil {
		return err
	}

	customer.Phone = newPhone

	cus_bytes, _ := json.Marshal(customer)

	return ctx.GetStub().PutState(cusKey, cus_bytes)
}

// DelRecord delete a record
func (s *SmartContract) DelRecord(ctx contractapi.TransactionContextInterface, cusKey string) error {
	_, err := s.SearchCusInfo(ctx, cusKey)

	if err != nil {
		return err
	}

	ctx.GetStub().DelState(cusKey)
	return nil
}

func main() {

	chaincode, err := contractapi.NewChaincode(new(SmartContract))

	if err != nil {
		fmt.Printf("Error create chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting chaincode: %s", err.Error())
	}
}
