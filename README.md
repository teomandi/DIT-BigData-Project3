# Page Rank

- Project 3 of Big Data subject
- Implemented by:
   - Theodoros Mandilaras
   - cs2.190018
- MSc DI/EKPA 2019-2020

---

Implementation and evaluation of two different PageRank algorithms on the **Google-web** dataset.

## Algorithm 1

### Simple PageRank equation

``p = M⋅p``

where **p** is a vector of size Nx1 (where N is the number of nodes in the graph). **p[i,1]** represents the
PageRank of page **i**. Initially every page’s PageRank is equal to 1. We repeat the above computation,
i.e., multiplying **M** with **p** and storing in **p** for a pre-specified number of steps.

## Algorithm 2

### Improved version of PageRank

``p = α⋅M⋅p + (1-α)⋅I​n``

where **α** is a numeric value, **N** is the number of pages (nodes) in the Web graph, and **In**​ is a unary
vector (i.e., all values are set to 1) of size Nx1.

---
