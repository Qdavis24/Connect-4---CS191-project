Connect Four Game

A Python implementation of the classic Connect Four game built with Tkinter for my CS-191 final project.

Description:

This project is a fully functional Connect Four game where two players take turns dropping colored coins into a grid. Players win by connecting four coins of their color either horizontally, vertically, or diagonally.

Features:

Graphical user interface built with Tkinter
Two-player gameplay with different colored coins (yellow and orange by default)
Win detection for horizontal, vertical, and diagonal connections
Victory animation with winning coins highlighted in red
Coin drop animation when game resets
Customizable board dimensions and colors

Technical Highlights:

Object-Oriented Design: Fully implemented using OOP principles with specialized classes for different game aspects
Custom Data Structures: State management using 2D arrays (nested lists in Python)
Advanced Algorithms: Multi-pointer approach for win detection logic
Complex Win Detection: Diagonal win checking using 4 pointers that traverse in each diagonal direction

Class Architecture:

PositionalMatrix

Manages geometric layout of the game board
Dynamically calculates and stores (x,y) coordinates for coin positions
Uses 2D array for coordinate matrix
Adapts to different board dimensions

StateMatrix

Handles game's logical state and win detection
Maintains game state using 2D array
Performs win-checking logic (horizontal, vertical, diagonal)
Manages piece placement and validation

Board

Manages all visual aspects using Tkinter
Handles drawing the game board and coins
Manages canvas elements and animations
Coordinates visual updates based on game state

Game

Acts as the main controller
Coordinates interactions between all classes
Handles user input events
Manages game flow and turn logic

How to Play

Run the game using Python 3.x
Click in any column to drop a coin
Players alternate turns until someone wins
A victory animation will play and the board will reset automatically

Requirements

Python 3.x
Tkinter (usually comes with Python installation)
