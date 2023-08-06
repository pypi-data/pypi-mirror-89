#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import src.day01 as d1


def main():
    expenses = d1.DayOne().import_expense_report("src/data/input.txt")
    d1.DayOne().answers(expenses)


if __name__ == '__main__':
    main()
