import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.BiFunction;
import java.util.function.Function;

public class Main {

	private Function<Integer, Integer> square = (a) -> a * a;
	private Function<Point, Integer> hashCoords = (p) -> 397 * p.x + p.y;
	private BiFunction<Point, Point, Integer> sqrDist = (a, b) -> square.apply(a.x - b.x) + square.apply(a.y - b.y);
	private int sqr_d12, sqr_d13, sqr_d14;

	class Point {
		int x, y;

		public Point(int x, int y) {
			this.x = x;
			this.y = y;
		}

		private float gradient(Point p) {
			float dx = x - p.x;
			return dx != 0 ? (y - p.y) / dx : Float.MAX_VALUE;
		}

		private float dotProd(Point p1, Point p2) {
			assert !p1.equals(this) && !p2.equals(this);
			return (p1.x - x) * (p2.x - x) + (p1.y - y) * (p2.y - y);
		}

		public float crossProd(Point p1, Point p2) {
			assert !p1.equals(this) && !p2.equals(this);
			return (p1.x - x) * (p2.y - y) - (p1.y - y) * (p2.x - x);
		}

		public boolean isRightAngDot(Point p1, Point p2) {
			assert !p1.equals(this) && !p2.equals(this);
			return dotProd(p1, p2) == 0;
		}

		public boolean isRightAngGrad(Point p1, Point p2) {
			float gradient_a = gradient(p1);
			float gradient_b = gradient(p2);
			if (gradient_a == 0) {
				return gradient_b == Float.MAX_VALUE;
			}
			if (gradient_b == 0) {
				return gradient_a == Float.MAX_VALUE;
			}
			return gradient_a * gradient_b == -1;
		}

		public boolean equalDistances(Point p1, Point p2) {
			return sqrDist.apply(this, p1) == sqrDist.apply(this, p2);
		}
	}

	private boolean isDivisible(int d, int div) {
		return (d %= div) == 0;
	}

	private boolean arePointsDistinct(int numPoints, Point... points) {
		Set<Integer> pointsSet = new HashSet<Integer>();
		Arrays.asList(points).forEach(p -> pointsSet.add(hashCoords.apply(p)));
		return pointsSet.size() == numPoints;
	}

	private boolean calculateSqrDistances(Point p1, Point p2, Point p3, Point p4) {
		if ((sqr_d12 = sqrDist.apply(p1, p2)) == 0)
			return false;
		if ((sqr_d13 = sqrDist.apply(p1, p3)) == 0)
			return false;
		if ((sqr_d14 = sqrDist.apply(p1, p4)) == 0)
			return false;
		return true;
	}

	boolean isSquareGradient(Point p1, Point p2, Point p3, Point p4) {
		if (!arePointsDistinct(4, p1, p2, p3, p4))
			return false;
		if (!calculateSqrDistances(p1, p2, p3, p4))
			return false;
		int area = Math.min(Math.min(sqr_d12, sqr_d13), sqr_d14);
		if (sqr_d14 == 2 * area) {
			return p2.isRightAngGrad(p1, p4) && p3.isRightAngGrad(p1, p4);
		}
		if (sqr_d13 == 2 * area) {
			return p2.isRightAngGrad(p1, p3) && p4.isRightAngGrad(p1, p3);
		}
		if (sqr_d12 == 2 * area) {
			return p3.isRightAngGrad(p1, p2) && p4.isRightAngGrad(p1, p2);
		}
		return false;
	}

	boolean isSquareDot(Point p1, Point p2, Point p3, Point p4) {
		if (!calculateSqrDistances(p1, p2, p3, p4))
			return false;
		int area = Math.min(Math.min(sqr_d12, sqr_d13), sqr_d14);
		if (sqr_d14 == 2 * area)
			return p1.isRightAngDot(p2, p3) && p4.isRightAngDot(p2, p3);
		if (sqr_d13 == 2 * area)
			return p1.isRightAngDot(p2, p4) && p3.isRightAngDot(p2, p4);
		if (sqr_d12 == 2 * area)
			return p1.isRightAngDot(p3, p4) && p2.isRightAngDot(p3, p4);
		return false;
	}

	boolean isSquareCross(Point p1, Point p2, Point p3, Point p4) {
		if (!arePointsDistinct(4, p1, p2, p3, p4))
			return false;
		if (p1.crossProd(p2, p3) == -p1.crossProd(p2, p4)) // ( p1, p2) is possible diagonal
			return p3.isRightAngDot(p1, p2) && p4.isRightAngDot(p1, p2) && p3.equalDistances(p1, p2);
		if (p1.crossProd(p3, p2) == -p1.crossProd(p3, p4)) // ( p1, p3) is possible diagonal
			return p2.isRightAngDot(p1, p3) && p4.isRightAngDot(p1, p3) && p2.equalDistances(p1, p3);
		if (p1.crossProd(p4, p2) == -p1.crossProd(p4, p3)) // ( p1, p4) is possible diagonal
			return p2.isRightAngDot(p1, p4) && p3.isRightAngDot(p1, p4) && p2.equalDistances(p1, p4);
		return false;
	}

	boolean isSquare(Point p1, Point p2, Point p3, Point p4) {
		if (!calculateSqrDistances(p1, p2, p3, p4))
			return false;
		int area = Math.min(Math.min(sqr_d12, sqr_d13), sqr_d14);
		if (!isDivisible(sqr_d12, area) || !isDivisible(sqr_d13, area) || !isDivisible(sqr_d14, area)
				|| (sqr_d12 + sqr_d13 + sqr_d14) != 4 * area) {
			return false;
		}
		if (sqr_d12 == 2 * area)
			return sqrDist.apply(p4, p3) == 2 * area && sqrDist.apply(p3, p2) == area
					&& sqrDist.apply(p4, p2) == area;
		if (sqr_d13 == 2 * area)
			return sqrDist.apply(p4, p2) == 2 * area && sqrDist.apply(p2, p3) == area
					&& sqrDist.apply(p4, p3) == area;
		if (sqr_d14 == 2 * area)
			return sqrDist.apply(p3, p2) == 2 * area && sqrDist.apply(p2, p4) == area
					&& sqrDist.apply(p3, p4) == area;
		return false;
	}

	boolean isSquareGeeksForGeeks(Point p1, Point p2, Point p3, Point p4) {
		int d2 = sqrDist.apply(p1, p2); // from p1 to p2
		int d3 = sqrDist.apply(p1, p3); // from p1 to p3
		int d4 = sqrDist.apply(p1, p4); // from p1 to p4
		if (d2 == 0 || d3 == 0 || d4 == 0)
			return false;
		// If lengths if (p1, p2) and (p1, p3) are same, then
		// following conditions must met to form a square.
		// 1) Square of length of (p1, p4) is same as twice
		// the square of (p1, p2)
		// 2) Square of length of (p2, p3) is same
		// as twice the square of (p2, p4)
		if (d2 == d3 && 2 * d2 == d4 && 2 * sqrDist.apply(p2, p4) == sqrDist.apply(p2, p3)) {
			return true;
		}
		// The below two cases are similar to above case
		if (d3 == d4 && 2 * d3 == d2 && 2 * sqrDist.apply(p3, p2) == sqrDist.apply(p3, p4)) {
			return true;
		}
		if (d2 == d4 && 2 * d2 == d3 && 2 * sqrDist.apply(p2, p3) == sqrDist.apply(p2, p4)) {
			return true;
		}
		return false;
	}

	public Main() {
		Point[][] squares = { { new Point(20, 10), new Point(10, 20), new Point(20, 20), new Point(10, 10) },
				{ new Point(1, 0), new Point(4, 1), new Point(3, 4), new Point(0, 3) },
				{ new Point(0, 0), new Point(3, 1), new Point(2, 4), new Point(-1, 3) },
				{ new Point(0, 0), new Point(1, 0), new Point(1, 1), new Point(0, 1) },
				{ new Point(0, -1), new Point(3, 0), new Point(2, 3), new Point(-1, 2) },
				{ new Point(3, 0), new Point(5, 2), new Point(3, 4), new Point(1, 2) },
				{ new Point(0, 0), new Point(2, 0), new Point(2, 2), new Point(0, 2) },
				{ new Point(0, 0), new Point(2, 1), new Point(3, -1), new Point(1, -2) },
				{ new Point(0, -2), new Point(2, 0), new Point(0, 2), new Point(-2, 0) } };

		Point[][] notSquares = { { new Point(20, 10), new Point(10, 20), new Point(20, 20), new Point(30, 10) },
				{ new Point(20, 10), new Point(10, 20), new Point(20, 20), new Point(-10, 10) },
				{ new Point(20, 10), new Point(20, 10), new Point(20, 10), new Point(20, 10) },
				{ new Point(3, 0), new Point(0, 0), new Point(6, -3), new Point(0, 3) },
				{ new Point(3, 0), new Point(3, 3), new Point(0, 6), new Point(0, 3) },
				{ new Point(3, 0), new Point(3, 3), new Point(3, 6), new Point(0, 3) },
				{ new Point(3, 0), new Point(3, 3), new Point(6, 6), new Point(6, 3) },
				{ new Point(-3, 6), new Point(3, 3), new Point(0, 0), new Point(0, 3) },
				{ new Point(3, 0), new Point(-3, -3), new Point(0, 0), new Point(0, 3) },
				{ new Point(3, 0), new Point(3, 3), new Point(6, 6), new Point(0, 3) },
				{ new Point(3, 0), new Point(5, 2), new Point(-1, 0), new Point(1, 2) },
				{ new Point(3, 0), new Point(3, 0), new Point(5, 2), new Point(1, 2) },
				{ new Point(3, 0), new Point(5, 2), new Point(3, 0), new Point(1, 2) },
				{ new Point(3, 0), new Point(5, 2), new Point(1, 2), new Point(3, 0) },
				{ new Point(1, 0), new Point(0, 1), new Point(0, 0), new Point(0, 0) },
				{ new Point(3, 0), new Point(5, 2), new Point(5, 2), new Point(1, 2) },
				{ new Point(3, 0), new Point(5, 2), new Point(1, 2), new Point(5, 2) },
				{ new Point(3, 0), new Point(1, 2), new Point(5, 2), new Point(5, 2) },
				{ new Point(0, 0), new Point(0, 0), new Point(0, 0), new Point(0, 0) },
				{ new Point(3, -1), new Point(5, 2), new Point(3, 4), new Point(1, 2) },
				{ new Point(3, -1), new Point(5, 2), new Point(3, 5), new Point(1, 2) },
				{ new Point(3, 0), new Point(6, 2), new Point(3, 4), new Point(0, 2) },
				{ new Point(0, 0), new Point(2, 0), new Point(2, 1), new Point(0, 1) },
				{ new Point(0, 2), new Point(2, 1), new Point(2, 3), new Point(0, 4) },
				{ new Point(-1, 0), new Point(2, 0), new Point(2, 1), new Point(-1, 1) },
				{ new Point(0, -2), new Point(2, 2), new Point(0, 2), new Point(-3, 1) },
				{ new Point(1, 1), new Point(4, 1), new Point(3, 4), new Point(0, 3) },
				{ new Point(0, 0), new Point(-3, 1), new Point(2, 4), new Point(-1, 3) },
				{ new Point(0, 0), new Point(1, 0), new Point(1, 1), new Point(1, 1) },
				{ new Point(0, -1), new Point(3, 0), new Point(2, 3), new Point(1, 2) },
				{ new Point(3, 0), new Point(3, 2), new Point(3, 4), new Point(1, 2) },
				{ new Point(0, 0), new Point(3, 0), new Point(2, 2), new Point(0, 2) },
				{ new Point(0, -2), new Point(2, 0), new Point(0, 2), new Point(-2, 1) } };

		int falseNegs = 0;
		int falsePostvs = 0;
//		System.out.println("Squares: ");
		for (Point[] square : squares) {
			List<Point> points = Arrays.asList(square);
			for (int i = 0; i < 4; i++, Collections.rotate(points, i)) {
				// points.forEach((p) -> System.out.printf("(%3d, %3d) ", p.x, p.y));
				// System.out.println();
				assert isSquare(points.get(0), points.get(1), points.get(2), points.get(3));
				assert isSquareCross(points.get(0), points.get(1), points.get(2), points.get(3));
				assert isSquareDot(points.get(0), points.get(1), points.get(2), points.get(3));
				assert isSquareGradient(points.get(0), points.get(1), points.get(2), points.get(3));
				falseNegs += !isSquareGeeksForGeeks(points.get(0), points.get(1), points.get(2), points.get(3))
						? 1
						: 0;
			}
		}

//		System.out.println("\nNot Squares: ");
		for (Point[] square : notSquares) {
			List<Point> points = Arrays.asList(square);
			for (int i = 0; i < 4; i++, Collections.rotate(points, i)) {
//				 points.forEach((p) -> System.out.printf("(%3d, %3d) ", p.x, p.y));
//				 System.out.println();
				assert !isSquare(points.get(0), points.get(1), points.get(2), points.get(3));
				assert !isSquareCross(points.get(0), points.get(1), points.get(2), points.get(3));
				assert !isSquareDot(points.get(0), points.get(1), points.get(2), points.get(3));
				assert !isSquareGradient(points.get(0), points.get(1), points.get(2), points.get(3));
				falsePostvs += isSquareGeeksForGeeks(points.get(0), points.get(1), points.get(2), points.get(3))
						? 1
						: 0;
			}
		}

		System.out.println();
		System.out.println("Errors in GeeksForGeeks solution:");
		System.out.println("False positives: " + falsePostvs);
		System.out.println("False negatives: " + falseNegs);
	}

  public static void main(String[] args) {
    new Main();
  }
}
