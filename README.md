# Traveling Salesperson Problem (with profits)
**Task:** Solving the Traveling Salesperson Problem with Profits

### Project Definition
In this project, I'm going to solve the traveling Salesperson problem with profits (TSPP) where the salesman collects some profit for visiting each customer. As opposed to the classical TSP, there is no requirement to visit all the customers. The objective of TSPP is to determine the best subset of customers to be visited so as to maximize the total net profit, which is equal to the total profit earned from visited customers less the total cost of the tour. The latter can be taken as the total length of the tour calculated as the Euclidean distance.

### Dataset
There are three data sets (eil51, eil76, eil101) given in each of the Excel files called “dataset-HighProfit.xls” and “dataset-LowProfit.xls”. The first one contains three data sets with high customer profits while the second one contains the same data sets, i.e., the same customer locations, but with low customer profits. The first customer is the depot location, i.e., the salesman starts its tour from this location. Therefore, the number of customers is equal to 50, 75, and 100 for eil51, eil76, and eil101 respectively. Hence, the input data consists of the customer locations and the profits associated with each customer. Please round all the Euclidean distances to two decimal points. The net profit should also be rounded to two decimal points.
