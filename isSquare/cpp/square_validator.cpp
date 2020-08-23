#include <iostream>
#include <stdio.h>
#include <assert.h>
#include <float.h> 
#include <set>
#include <vector>
#include <algorithm>

class Point
{
private:
	float gradient(Point p);
	float dotProd(Point p1, Point p2);
public:
	int x, y;
	Point(int x, int y);
	float crossProd(Point p1, Point p2);
	bool isRightAngDot(Point p1, Point p2);
	bool isRightAngGrad(Point p1, Point p2);
	bool equalDistances(Point p1, Point p2);
};

class SquareValidator
{
private:
	int sqr_d12, sqr_d13, sqr_d14;
	bool isDivisible(int d, int div);
	bool arePointsDistinct(std::vector<Point> points);
	bool calculateSqrDistances(Point p1, Point p2, Point p3, Point p4);
public:
	SquareValidator();
	bool isSquareGradient(Point p1, Point p2, Point p3, Point p4);
	bool isSquareDot(Point p1, Point p2, Point p3, Point p4);
	bool isSquareCross(Point p1, Point p2, Point p3, Point p4);
	bool isSquare(Point p1, Point p2, Point p3, Point p4);
	bool isSquareGeeksForGeeks(Point p1, Point p2, Point p3, Point p4);
};

constexpr auto square = [](int a) { return a * a; };
constexpr auto sqrDist = [](Point a, Point b) {return square(a.x - b.x) + square(a.y - b.y); };
constexpr auto hashCoords = [](Point p) { return 397 * p.x + p.y; };

Point::Point(int x, int y)
{
	this->x = x;
	this->y = y;
}

float Point::crossProd(Point p1, Point p2)
{
	return (p1.x - x) * (p2.y - y) - (p1.y - y) * (p2.x - x);
}

bool Point::isRightAngDot(Point p1, Point p2)
{
	return dotProd(p1, p2) == 0;
}

bool Point::isRightAngGrad(Point p1, Point p2)
{
	float gradient_a = gradient(p1);
	float gradient_b = gradient(p2);
	if (gradient_a == 0)
	{
		return gradient_b == FLT_MAX;
	}
	if (gradient_b == 0)
	{
		return gradient_a == FLT_MAX;
	}
	return gradient_a * gradient_b == -1;
}

bool Point::equalDistances(Point p1, Point p2)
{
	return sqrDist(*this, p1) == sqrDist(*this, p2);
}

float Point::gradient(Point p)
{
	float dx = x - p.x;
	return dx != 0 ? (y - p.y) / dx : FLT_MAX;
}

float Point::dotProd(Point p1, Point p2)
{
	return (p1.x - x) * (p2.x - x) + (p1.y - y) * (p2.y - y);
}


bool SquareValidator::isDivisible(int d, int div)
{
	return (d %= div) == 0;
}

bool SquareValidator::arePointsDistinct(std::vector<Point> points_v)
{
	std::set<int> points_set;
	std::for_each(points_v.begin(), points_v.end(), [&points_set](Point p) {points_set.insert(hashCoords(p));});
	return points_set.size() == points_v.size();
}

bool SquareValidator::calculateSqrDistances(Point p1, Point p2, Point p3, Point p4)
{
	if ((sqr_d12 = sqrDist(p1, p2)) == 0)
		return false;
	if ((sqr_d13 = sqrDist(p1, p3)) == 0)
		return false;
	if ((sqr_d14 = sqrDist(p1, p4)) == 0)
		return false;
	return true;
}

bool SquareValidator::isSquareGradient(Point p1, Point p2, Point p3, Point p4)
{
	if (!arePointsDistinct({p1, p2, p3, p4}))
		return false;
	if (!calculateSqrDistances(p1, p2, p3, p4))
		return false;
	int area = std::min(std::min(sqr_d12, sqr_d13), sqr_d14);
	if (sqr_d14 == 2 * area)
	{
		return p2.isRightAngGrad(p1, p4) && p3.isRightAngGrad(p1, p4);
	}
	if (sqr_d13 == 2 * area)
	{
		return p2.isRightAngGrad(p1, p3) && p4.isRightAngGrad(p1, p3);
	}
	if (sqr_d12 == 2 * area)
	{
		return p3.isRightAngGrad(p1, p2) && p4.isRightAngGrad(p1, p2);
	}
	return false;
}

bool SquareValidator::isSquareDot(Point p1, Point p2, Point p3, Point p4)
{
	if (!calculateSqrDistances(p1, p2, p3, p4))
		return false;
	int area = std::min(std::min(sqr_d12, sqr_d13), sqr_d14);
	if (sqr_d14 == 2 * area)
		return p1.isRightAngDot(p2, p3) && p4.isRightAngDot(p2, p3);
	if (sqr_d13 == 2 * area)
		return p1.isRightAngDot(p2, p4) && p3.isRightAngDot(p2, p4);
	if (sqr_d12 == 2 * area)
		return p1.isRightAngDot(p3, p4) && p2.isRightAngDot(p3, p4);
	return false;
}

bool SquareValidator::isSquareCross(Point p1, Point p2, Point p3, Point p4)
{
	if (!arePointsDistinct({p1, p2, p3, p4}))
		return false;
	if (p1.crossProd(p2, p3) == -p1.crossProd(p2, p4)) // ( p1, p2) is possible diagonal
		return p3.isRightAngDot(p1, p2) && p4.isRightAngDot(p1, p2) && p3.equalDistances(p1, p2);
	if (p1.crossProd(p3, p2) == -p1.crossProd(p3, p4)) // ( p1, p3) is possible diagonal
		return p2.isRightAngDot(p1, p3) && p4.isRightAngDot(p1, p3) && p2.equalDistances(p1, p3);
	if (p1.crossProd(p4, p2) == -p1.crossProd(p4, p3)) // ( p1, p4) is possible diagonal
		return p2.isRightAngDot(p1, p4) && p3.isRightAngDot(p1, p4) && p2.equalDistances(p1, p4);
	return false;
}

bool SquareValidator::isSquare(Point p1, Point p2, Point p3, Point p4)
{
	if (!calculateSqrDistances(p1, p2, p3, p4))
		return false;
	int area = std::min(std::min(sqr_d12, sqr_d13), sqr_d14);
	if (!isDivisible(sqr_d12, area) || !isDivisible(sqr_d13, area) || !isDivisible(sqr_d14, area) || (sqr_d12 + sqr_d13 + sqr_d14) != 4 * area)
		return false;
	if (sqr_d12 == 2 * area)
		return sqrDist(p4, p3) == 2 * area && sqrDist(p3, p2) == area && sqrDist(p4, p2) == area;
	if (sqr_d13 == 2 * area)
		return sqrDist(p4, p2) == 2 * area && sqrDist(p2, p3) == area && sqrDist(p4, p3) == area;
	if (sqr_d14 == 2 * area)
		return sqrDist(p3, p2) == 2 * area && sqrDist(p2, p4) == area && sqrDist(p3, p4) == area;
	return false;
}

bool SquareValidator::isSquareGeeksForGeeks(Point p1, Point p2, Point p3, Point p4)
{
	int d2 = sqrDist(p1, p2); // from p1 to p2
	int d3 = sqrDist(p1, p3); // from p1 to p3
	int d4 = sqrDist(p1, p4); // from p1 to p4
	if (d2 == 0 || d3 == 0 || d4 == 0)
		return false;
	// If lengths if (p1, p2) and (p1, p3) are same, then
	// following conditions must met to form a square.
	// 1) Square of length of (p1, p4) is same as twice
	// the square of (p1, p2)
	// 2) Square of length of (p2, p3) is same
	// as twice the square of (p2, p4)
	if (d2 == d3 && 2 * d2 == d4 && 2 * sqrDist(p2, p4) == sqrDist(p2, p3))
		return true;
	// The below two cases are similar to above case
	if (d3 == d4 && 2 * d3 == d2 && 2 * sqrDist(p3, p2) == sqrDist(p3, p4))
		return true;
	if (d2 == d4 && 2 * d2 == d3 && 2 * sqrDist(p2, p3) == sqrDist(p2, p4))
		return true;
	return false;
}

SquareValidator::SquareValidator()
{
	std::vector<std::vector<Point>> squares{{Point(20, 10), Point(10, 20), Point(20, 20), Point(10, 10)},
	{Point(1, 0), Point(4, 1), Point(3, 4), Point(0, 3)},
	{Point(0, 0), Point(3, 1), Point(2, 4), Point(-1, 3)},
	{Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)},
	{Point(0, -1), Point(3, 0), Point(2, 3), Point(-1, 2)},
	{Point(3, 0), Point(5, 2), Point(3, 4), Point(1, 2)},
	{Point(0, 0), Point(2, 0), Point(2, 2), Point(0, 2)},
	{Point(0, 0), Point(2, 1), Point(3, -1), Point(1, -2)},
	{Point(0, -2), Point(2, 0), Point(0, 2), Point(-2, 0)}};

	std::vector<std::vector<Point>>  notSquares{{Point(20, 10), Point(10, 20), Point(20, 20), Point(30, 10)},
	{Point(20, 10), Point(10, 20), Point(20, 20), Point(-10, 10)},
	{Point(20, 10), Point(20, 10), Point(20, 10), Point(20, 10)},
	{Point(3, 0), Point(0, 0), Point(6, -3), Point(0, 3)},
	{Point(3, 0), Point(3, 3), Point(0, 6), Point(0, 3)},
	{Point(3, 0), Point(3, 3), Point(3, 6), Point(0, 3)},
	{Point(3, 0), Point(3, 3), Point(6, 6), Point(6, 3)},
	{Point(-3, 6), Point(3, 3), Point(0, 0), Point(0, 3)},
	{Point(3, 0), Point(-3, -3), Point(0, 0), Point(0, 3)},
	{Point(3, 0), Point(3, 3), Point(6, 6), Point(0, 3)},
	{Point(3, 0), Point(5, 2), Point(-1, 0), Point(1, 2)},
	{Point(3, 0), Point(3, 0), Point(5, 2), Point(1, 2)},
	{Point(3, 0), Point(5, 2), Point(3, 0), Point(1, 2)},
	{Point(3, 0), Point(5, 2), Point(1, 2), Point(3, 0)},
	{Point(1, 0), Point(0, 1), Point(0, 0), Point(0, 0)},
	{Point(3, 0), Point(5, 2), Point(5, 2), Point(1, 2)},
	{Point(3, 0), Point(5, 2), Point(1, 2), Point(5, 2)},
	{Point(3, 0), Point(1, 2), Point(5, 2), Point(5, 2)},
	{Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)},
	{Point(3, -1), Point(5, 2), Point(3, 4), Point(1, 2)},
	{Point(3, -1), Point(5, 2), Point(3, 5), Point(1, 2)},
	{Point(3, 0), Point(6, 2), Point(3, 4), Point(0, 2)},
	{Point(0, 0), Point(2, 0), Point(2, 1), Point(0, 1)},
	{Point(0, 2), Point(2, 1), Point(2, 3), Point(0, 4)},
	{Point(-1, 0), Point(2, 0), Point(2, 1), Point(-1, 1)},
	{Point(0, -2), Point(2, 2), Point(0, 2), Point(-3, 1)},
	{Point(1, 1), Point(4, 1), Point(3, 4), Point(0, 3)},
	{Point(0, 0), Point(-3, 1), Point(2, 4), Point(-1, 3)},
	{Point(0, 0), Point(1, 0), Point(1, 1), Point(1, 1)},
	{Point(0, -1), Point(3, 0), Point(2, 3), Point(1, 2)},
	{Point(3, 0), Point(3, 2), Point(3, 4), Point(1, 2)},
	{Point(0, 0), Point(3, 0), Point(2, 2), Point(0, 2)},
	{Point(0, -2), Point(2, 0), Point(0, 2), Point(-2, 1)}};

	int falseNegs = 0;
	int falsePostvs = 0;
	// std::cout << "Squares: " << std::endl;
	for (auto points : squares)
	{
		for (int i = 0; i < 4; i++, std::rotate(points.begin(), points.begin() + i, points.end()))
		{
			// for (auto point : points)
			// 	std::cout << "(" << point.x << ", " << point.y << ") ";
			// std::cout << std::endl;
			assert(isSquare(points[0], points[1], points[2], points[3]));
			assert(isSquareCross(points[0], points[1], points[2], points[3]));
			assert(isSquareDot(points[0], points[1], points[2], points[3]));
			assert(isSquareGradient(points[0], points[1], points[2], points[3]));
			falseNegs += !isSquareGeeksForGeeks(points[0], points[1], points[2], points[3])
			? 1
			: 0;
		}
	}

	// std::cout << "\nNot Squares: " << std::endl;
	for (auto points : notSquares) 
	{
		for (int i = 0; i < 4; i++, std::rotate(points.begin(), points.begin() + i, points.end()))
		{
			// for (auto point : points)
			// 	std::cout << "(" << point.x << ", " << point.y << ") ";
			// std::cout << std::endl;
			assert(!isSquare(points[0], points[1], points[2], points[3]));
			assert(!isSquareCross(points[0], points[1], points[2], points[3]));
			assert(!isSquareDot(points[0], points[1], points[2], points[3]));
			assert(!isSquareGradient(points[0], points[1], points[2], points[3]));
			falsePostvs += isSquareGeeksForGeeks(points[0], points[1], points[2], points[3])
			? 1
			: 0;
		}
	}

	std::cout << std::endl;
	std::cout << "Errors in GeeksForGeeks solution:" << std::endl;
	std::cout << "False positives: " << falsePostvs << std::endl;
	std::cout << "False negatives: " << falseNegs << std::endl;
}


int main()
{
	SquareValidator square_validator;
	return 0;
}
