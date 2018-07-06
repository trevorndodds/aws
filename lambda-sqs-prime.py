from __future__ import print_function

import json
import urllib
import boto3
import time
import math

def lambda_handler(event, context):
    #print (event)
    body = event['Records'][0]['body']
    messageId = event['Records'][0]['messageId']
    calcType = event['Records'][0]['messageAttributes']['calcType']['stringValue']
    primenum = int(event['Records'][0]['messageAttributes']['primes']['stringValue'])
    print ('Body: ' + body)
    print ('messageId: ' + str(messageId))
    print ('calcType: ' + calcType)
    print ('primenum:' + str(primenum))
    if calcType == "calcPrimeTo":
        calcPrimeTo(primenum)
    elif calcType == "calcPrimeWithin":
        calcPrimeWithin(primenum)
    else:
        print ("Method not Found")
    #return event

def calcPrimeWithin(n):
    try:
        now = time.time()
        primes = [2]
        nextPrime = 3
        while nextPrime < n:
            isPrime = True
            i = 0
            sqrt = math.sqrt(nextPrime)
            while primes[i] <= sqrt:
                if nextPrime % primes[i] == 0:
                    isPrime = False
                i += 1
            if isPrime:
                primes.append(nextPrime)
            nextPrime += 2
        #print (primes)
        elapsed = time.time() - now
        print ('Total calcPrimeWithin Time: ' + str(elapsed))
        print ('Found ' +  str(len(primes)) + ' Primes in ' +  str(n) + ' numbers')
    except Exception as e:
        print(e)
        

def calcPrimeTo(n):
    try:
        now = time.time()
        primes = [2]
        nextPrime = 3
        while len(primes) < n:
            isPrime = True
            i = 0
            sqrt = math.sqrt(nextPrime)
            while primes[i] <= sqrt:
                if nextPrime % primes[i] == 0:
                    isPrime = False
                i += 1
            if isPrime:
                primes.append(nextPrime)
            nextPrime += 2
        #print primes
        elapsed = time.time() - now
        print ('Total calcPrimeWithin Time: ' + str(elapsed))
        print ('Found ' +  str(len(primes)) + ' Primes in ' +  str(n) + ' numbers')
    except Exception as e:
        print(e)
