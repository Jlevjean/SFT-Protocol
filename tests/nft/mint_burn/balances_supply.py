#!/usr/bin/python3

from brownie import *
from scripts.deployment import main


def setup():
    config['test']['always_transact'] = False
    main(NFToken)
    global token, issuer
    token = NFToken[0]
    issuer = IssuingEntity[0]


def mint_to_issuer():
    '''mint to issuer'''
    token.mint(issuer, 1000, 0, "0x00", {'from': a[0]})
    check.equal(token.totalSupply(), 1000)
    check.equal(token.balanceOf(issuer), 1000)
    token.mint(issuer, 2000, 0, "0x00", {'from': a[0]})
    check.equal(token.totalSupply(), 3000)
    check.equal(token.balanceOf(issuer), 3000)


def mint_to_investors():
    '''mint to investors'''
    token.mint(a[1], 1000, 0, "0x00", {'from': a[0]})
    check.equal(token.totalSupply(), 1000)
    check.equal(token.balanceOf(a[1]), 1000)
    token.mint(a[2], 2000, 0, "0x00", {'from': a[0]})
    check.equal(token.totalSupply(), 3000)
    check.equal(token.balanceOf(a[1]), 1000)
    check.equal(token.balanceOf(a[2]), 2000)
    token.mint(a[1], 3000, 0, "0x00", {'from': a[0]})
    check.equal(token.totalSupply(), 6000)
    check.equal(token.balanceOf(a[1]), 4000)
    check.equal(token.balanceOf(a[2]), 2000)
    token.mint(a[2], 4000, 0, "0x00", {'from': a[0]})
    check.equal(token.totalSupply(), 10000)
    check.equal(token.balanceOf(a[1]), 4000)
    check.equal(token.balanceOf(a[2]), 6000)


def burn_from_issuer():
    '''burn from issuer'''
    token.mint(issuer, 10000, 0, "0x00", {'from': a[0]})
    token.burn(1, 1001, {'from': a[0]})
    check.equal(token.totalSupply(), 9000)
    check.equal(token.balanceOf(issuer), 9000)
    token.burn(1001, 5001, {'from': a[0]})
    check.equal(token.totalSupply(), 5000)
    check.equal(token.balanceOf(issuer), 5000)
    token.burn(5001, 10001, {'from': a[0]})
    check.equal(token.totalSupply(), 0)
    check.equal(token.balanceOf(issuer), 0)


def burn_from_investors():
    '''burn from investors'''
    token.mint(a[1], 5000, 0, "0x00", {'from': a[0]})
    token.mint(a[2], 10000, 0, "0x00", {'from': a[0]})
    token.burn(3001, 5001, {'from': a[0]})
    check.equal(token.totalSupply(), 13000)
    check.equal(token.balanceOf(a[1]), 3000)
    check.equal(token.balanceOf(a[2]), 10000)
    token.burn(5001, 8001, {'from': a[0]})
    check.equal(token.totalSupply(), 10000)
    check.equal(token.balanceOf(a[1]), 3000)
    check.equal(token.balanceOf(a[2]), 7000)
    token.burn(1, 3001, {'from': a[0]})
    check.equal(token.totalSupply(), 7000)
    check.equal(token.balanceOf(a[1]), 0)
    check.equal(token.balanceOf(a[2]), 7000)
    token.burn(8001, 15001, {'from': a[0]})
    check.equal(token.totalSupply(), 0)
    check.equal(token.balanceOf(a[1]), 0)
    check.equal(token.balanceOf(a[2]), 0)


def authorized_supply():
    '''modify authorized supply'''
    token.modifyAuthorizedSupply(10000, {'from': a[0]})
    check.equal(token.authorizedSupply(), 10000)
    check.equal(token.totalSupply(), 0)
    token.modifyAuthorizedSupply(0, {'from': a[0]})
    check.equal(token.authorizedSupply(), 0)
    check.equal(token.totalSupply(), 0)
    token.modifyAuthorizedSupply(1234567, {'from': a[0]})
    check.equal(token.authorizedSupply(), 1234567)
    check.equal(token.totalSupply(), 0)
    token.modifyAuthorizedSupply(2400000000, {'from': a[0]})
    check.equal(token.authorizedSupply(), 2400000000)
    check.equal(token.totalSupply(), 0)


def mint_zero():
    '''mint, burn, mint'''
    token.mint(issuer, 10000, 0, "0x00", {'from': a[0]})
    check.equal(token.totalSupply(), 10000)
    token.burn(1, 10001, {'from': a[0]})
    check.equal(token.totalSupply(), 0)
    token.mint(issuer, 10000, 0, "0x00", {'from': a[0]})
    check.equal(token.totalSupply(), 10000)
    check.equal(token.rangesOf(issuer), ((10001, 20001,),))
    check.equal(
        token.getRange(1)[0],
        '0x0000000000000000000000000000000000000000'
    )