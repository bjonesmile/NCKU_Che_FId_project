import numpy as np
import geatpy as ea
import sys
from math import gcd as builtin_gcd
 
def gcd(a, *r):
  for b in r:
    a = builtin_gcd(a, b)
  return a
 
def lcm(a, *r):
  for b in r:
    a *= b // builtin_gcd(a, b)
  return abs(a)
 
def frobenius_number(a):
  def __residue_table(a):
    n = [0] + [None] * (a[0] - 1)
    for i in range(1, len(a)):
      d = gcd(a[0], a[i])
      for r in range(d):
        try:
          nn = min(n[q] for q in range(r, a[0], d) if n[q] is not None)
        except ValueError:
          continue
        if nn is not None:
          for c in range(a[0] // d):
            nn += a[i]
            p = nn % a[0]
            nn = min(nn, n[p]) if n[p] is not None else nn
            n[p] = nn
    return n
 
  if len(a) < 2 or gcd(*a) > 1:
    raise ValueError
  return max(__residue_table(sorted(a))) - min(a)
 
def frobenius_solve(a, m):
  def __extended_residue_table(a):
    n = [[0] + [None] * (a[0] - 1)]
    for i in range(1, len(a)):
      n.append(n[-1][:])
      d = gcd(a[0], a[i])
      for r in range(d):
        try:
          nn = min(n[-1][q] for q in range(r, a[0], d) if n[-1][q] is not None)
        except ValueError:
          continue
        if nn is not None:
          for c in range(a[0] // d):
            nn += a[i]
            p = nn % a[0]
            nn = min(nn, n[-1][p]) if n[-1][p] is not None else nn
            n[-1][p] = nn
    return n
 
  def __frobenius_recurse(a, m, ert, c, i):
    if i == 0:
      c[0] = m // a[0]
      yield tuple(c)
    else:
      lc = lcm(a[0], a[i])
      l = lc // a[i]
      for j in range(l):
        c[i] = j
        mm = m - j * a[i]
        r = mm % a[0]
        lb = ert[i - 1][r]
        if lb is not None:
          while mm >= lb:
            yield from __frobenius_recurse(a, mm, ert, c, i - 1)
            mm -= lc
            c[i] += l
 
  g = gcd(*a)
  if m <= 0 or len(a) < 2 or g > 1 and m % g:
    return
  if g > 1:
    a, m = sorted(x // g for x in a), m // g
  ert = __extended_residue_table(a)
  c = [0] * len(a)
  yield from __frobenius_recurse(a, m, ert, c, len(a) - 1)
