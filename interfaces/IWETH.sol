// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

interface IWETH {
    function deposit() external payable;
    function withdraw(uint256 amount) external payable;
    function balanceOf(address holder) external view returns(uint256 balance);
    function approve(address spender, uint256 amount) external;
}