#pragma once

#include <tinygeo/concepts.h>
#include <tinygeo/buffer.h>
#include <Eigen/Dense>

namespace tinygeo {
	
template<typename Num, typename Tag>
struct RaytraceResult {
	Num lambda;
	std::vector<Tag> tags;
	
	RaytraceResult() :
		lambda(std::numeric_limits<Num>::infinity()),
		tags()
	{}
	
	RaytraceResult(Num lambda, const std::vector<Tag>& tags = std::vector<Tag>()) :
		lambda(lambda),
		tags(tags)
	{}
	
	void combine(const RaytraceResult<Num, Tag>& other) {
		if(other.lambda >= lambda)
			return;
		
		lambda = other.lambda;
		tags = other.tags;
	}
	
	RaytraceResult<Num, Tag>& operator<<(const RaytraceResult<Num, Tag>& other) {
		combine(other);
		return *this;
	}
};

template<typename X>
using raytrace_result_for = RaytraceResult<typename X::Point::numeric_type, typename X::tag_type>;

template<typename X, bool enif>
using conditional_raytrace = std::enable_if_t<enif, raytrace_result_for<X>>;
	
template<typename T>
struct same_type { using type = T; };

template<typename T>
using same_type_t = typename same_type<T>::type;

template<typename N>
conditional_raytrace<N, N::tag == tags::node> ray_trace(
	const point_for<typename N::Point>& start,
	const point_for<typename N::Point>& end,
	const N& node,
	typename N::Point::numeric_type l_max
) {
	using Num = typename N::Point::numeric_type;
	using Tag = typename N::tag_type;
	using PairType = std::pair<Num, size_t>;
	
	//pybind11::print("Casting ray through node");
	//pybind11::print("  with " + std::to_string(node.n_data()) + " triangles");
	//pybind11::print("  with " + std::to_string(node.n_children()) + " children");
	
	// Intersect with stored triangles
	//Num result = std::numeric_limits<Num>::infinity();
	RaytraceResult<Num, Tag> result;
	{
		std::vector<PairType> data;
		data.reserve(node.n_data());
		for(size_t i = 0; i < node.n_data(); ++i)
			data.push_back(std::make_pair(ray_trace(start, end, node.data(i).bounding_box(), l_max).lambda, i));
		
		std::sort(data.begin(), data.end());
		
		for(size_t i = 0; i < data.size(); ++i) {
			if(data[i].first < std::min(result.lambda, l_max)) {
				/*Num it_result = ray_trace(start, end, node.data(data[i].second), l_max);
				result = std::min(result, it_result);*/
				result << ray_trace(start, end, node.data(data[i].second), l_max);
			} else {
				continue;
			}
		}
	}
	
	//pybind11::print("  after children, result is " + std::to_string(result));
	
	// Compute lower bound on distance based on bounding box intersections
	{
		std::vector<PairType> data;
		data.reserve(node.n_children());
		for(size_t i = 0; i < node.n_children(); ++i)
			data.push_back(std::make_pair(ray_trace(start, end, node.child(i).bounding_box(), l_max).lambda, i));
		
		std::sort(data.begin(), data.end());
		
		for(size_t i = 0; i < node.n_children(); ++i) {
			//pybind11::print("  Intersection with bounding box " + std::to_string(data[i].second) + ": " + std::to_string(data[i].first));
			
			if(data[i].first < std::min(result.lambda, l_max)) {
				//pybind11::print("  Promising. Proceeding with child");
				/*Num it_result = ray_trace(start, end, node.child(data[i].second), l_max);
				//pybind11::print("  Child returned " + std::to_string(it_result));
				result = std::min(result, it_result);*/
				result << ray_trace(start, end, node.child(data[i].second), l_max);
				//pybind11::print("  New threshold: " + std::to_string(result));
			} else {
				//pybind11::print("  Limit exceeded. Returning " + std::to_string(result));
				//pybind11::print("  Limit exceeded. Trying anyway");
				//Num it_result = ray_trace(start, end, node.child(data[i].second), l_max);
				//pybind11::print("  Child returned " + std::to_string(it_result));
				continue;
			}
		}
	}
	
	//pybind11::print("  All boxed processed. Returning " + std::to_string(result));
	
	return result;
}

template<typename G>
conditional_raytrace<G, G::tag == tags::grid> ray_trace(
	const point_for<typename G::Point>& start,
	const point_for<typename G::Point>& end,
	const G& grid,
	typename G::Point::numeric_type l_max
) {
	using P = typename G::Point;
	using Num = typename P::numeric_type;
	using Tag = typename G::tag_type;
	constexpr size_t dim = P::dimension;
	
	using MultiIndex = typename G::MultiIndex;
	
	MultiIndex i1 = grid.index_for(start);
	MultiIndex i2 = grid.index_for(end);
	
	/*pybind11::print("P1: ");
	for(size_t d = 0; d < dim; ++d)
		pybind11::print("\t", start[d]);
	pybind11::print("P2: ");
	for(size_t d = 0; d < dim; ++d)
		pybind11::print("\t", end[d]);
	
	pybind11::print("i1: ", i1);
	pybind11::print("i2: ", i2);*/
	
	const auto children = grid.query(i1, i2);
	
	//pybind11::print("Query hit", children.size(), " results");
	
	//Num result = std::numeric_limits<Num>::infinity();
	RaytraceResult<Num, Tag> result;
	for(const auto child : children) {
		auto bb = child.bounding_box();
		
		Num box_hit = ray_trace(start, end, child.bounding_box(), l_max).lambda;
		//if(box_hit < std::numeric_limits<Num>::infinity())
		//	pybind11::print("Box hit at ", box_hit);
		
		if(!(box_hit < result.lambda))
			continue;
		
		result << ray_trace(start, end, child, l_max);
	}
	
	return result;
}

template<typename B>
conditional_raytrace<B, B::tag == tags::box> ray_trace(
	const point_for<typename B::Point>& start,
	const point_for<typename B::Point>& end,
	const B& box,
	typename B::Point::numeric_type l_max
) {
	using PB = typename B::Point;
	using Num = typename PB::numeric_type;
	using Tag = typename B::tag_type;
	constexpr size_t dim = PB::dimension;
	
	const PB p1 = box.min();
	const PB p2 = box.max();
	
	const Num inf = std::numeric_limits<Num>::infinity();
	const Num tol = 5 * std::numeric_limits<Num>::epsilon();
	
	// We need to check for the empty box
	if(is_empty(box))
		return inf;
	
	Num lower_bound = 0;
	Num upper_bound = inf;	
	
	for(size_t i = 0; i < dim; ++i) {
		Num i_low;
		Num i_high;
		
		// In case we don't point in the i'th direction, we have to see whether we are inside the box
		// If we are, any value is OK
		// If we are not, none is
		if(std::abs(end[i] - start[i]) <= tol) {
			if((p1[i] - start[i]) * (p2[i] - start[i]) <= 0) {
				i_low = -inf;
				i_high = inf;
			} else {
				i_low = inf;
				i_high = -inf;
			}
		} else {
			const Num l1 = (p1[i] - start[i]) / (end[i] - start[i]);
			const Num l2 = (p2[i] - start[i]) / (end[i] - start[i]);
			
			if(l1 < l2) {
				i_low = l1; i_high = l2;
			} else {
				i_low = l2; i_high = l1;
			}
		}
		
		// Reduction
		lower_bound = std::max(lower_bound, i_low);
		upper_bound = std::min(upper_bound, i_high);
	}
	
	if(lower_bound > upper_bound)
		return inf;
	
	if(lower_bound > l_max)
		return inf;
	
	return RaytraceResult<Num, Tag>(lower_bound);
}

template<typename T>
conditional_raytrace<T, T::tag == tags::triangle && T::Point::dimension == 3> ray_trace(const point_for<typename T::Point>& start, const point_for<typename T::Point>& end, const T& tri, typename T::Point::numeric_type l_max) {
	using P = typename T::Point;
	using Num = typename P::numeric_type;
	using Tag = typename T::tag_type;
	using Mat = Eigen::Matrix<Num, 3, 3>;
	using Vec = Eigen::Matrix<Num, 3, 1>;
		
	Mat m;
	for(size_t i = 0; i < 3; ++i) {
		m(i, 0) = end[i] - start[i];
		m(i, 1) = tri.template get<1>()[i] - tri.template get<0>()[i];
		m(i, 2) = tri.template get<2>()[i] - tri.template get<0>()[i];
	}
	
	/*pybind11::print("INT matrix");
	{
		std::stringstream ss;
		ss << m;
		pybind11::print(ss.str());
	}*/
	
	Vec v;
	for(size_t i = 0; i < 3; ++i) {
		v(i, 0) = start[i] - tri.template get<0>()[i];
	}
	
	/*pybind11::print("INT vec");
	{
		std::stringstream ss;
		ss << v;
		pybind11::print(ss.str());
	}*/
	
	Vec vi = m.partialPivLu().solve(v);
	
	const Num l = -vi(0, 0);
	const Num inf = std::numeric_limits<Num>::infinity();
	
	// Check if we didn't hit the triangle plane
	if(l > l_max || l < 0)
		return RaytraceResult<Num, Tag>();
	
	// Check if we missed the triangle
	if(vi(1, 0) < 0 || vi(2, 0) < 0 || vi(1, 0) + vi(2, 0) > 1)
		return RaytraceResult<Num, Tag>();
	
	return RaytraceResult<Num, Tag>(l, tri.tags());
}

template<typename T>
conditional_raytrace<T, T::tag == tags::triangle && T::Point::dimension != 3> ray_trace(const point_for<typename T::Point>& start, const point_for<typename T::Point>& end, const T& tri, typename T::Point::numeric_type l_max) {
	throw std::runtime_error("Not implemented");
}


/*template<typename T>
typename std::enable_if_t<
	T::tag == tags::triangle && T::Point::dimension == 2,
	typename T::Point::numeric_type
> ray_trace(const typename T::Point& start, const typename T::Point& end, const T& tri, typename T::Point::numeric_type l_max) {
	using P = typename T::Point;
	using Num = typename P::numeric_type;
	
	using PMat = Eigen::Matrix<Num, 4, 2>;
	PMat m;
	
	m(0, 0) = end[0] - start[0];
	m(0, 1) = end[1] - start[1];
	m(1, 0) = tri.get<1>[1] - tri.get<0>[1];
	m(1, 1) = tri.get<0>[0] - tri.get<1>[0];
	m(2, 0) = tri.get<2>[1] - tri.get<0>[1];
	m(2, 1) = tri.get<0>[0] - tri.get<2>[0];
	m(3, 0) = tri.get<2>[1] - tri.get<1>[1];
	m(3, 1) = tri.get<1>[0] - tri.get<2>[0];
	
	Eigen::Matrix<Num, 2, 2> eline;
	eline(0, 0) = start[0];
	eline(1, 0) = start[1];
	eline(0, 1) = end[0];
	eline(1, 1) = end[1];
	
	Eigen::Matrix<Num, 2, 3> etri;
	eline(0, 0) = tri.get<0>[0];
	eline(1, 0) = tri.get<0>[1];
	eline(0, 1) = tri.get<1>[0];
	eline(1, 1) = tri.get<1>[1];
	eline(0, 2) = tri.get<2>[0];
	eline(1, 2) = tri.get<2>[1];
	
	auto p_line = m * eline;
	auto p_tri  = m * etri;
	
	if((p_line.rowwise().maxCoeff() > p_tri.rowwise().minCoeff() && p
}*/
}