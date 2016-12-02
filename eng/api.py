from flask import Blueprint, jsonify, request
from flask_restful import Resource, Api
import json
import eng.mvbridge as mvb
import eng.beam as beam
import eng.deflected_shape as deflected_shape

eng_api = Api(Blueprint('eng_api', __name__))

@eng_api.resource('/mvbridge')
class MVBridge(Resource):
    def get(self):
        span_length = request.args.get('spanLength', 'error', type=float)
        x_loc = request.args.get('xLoc', 'error', type=float)
        feet_or_frac = request.args.get('feetOrFrac', 'feet', type=str)
        incr = request.args.get('increment', 'error', type=float)
        impact_factor = request.args.get('impactFactor', 'error', type=float)
        dist_factor = request.args.get('distFactor', 'error', type=float)
        results = mvb.max_mv_bridge(span_length, x_loc, feet_or_frac, incr,
                                impact_factor, dist_factor)
        return jsonify(results)


@eng_api.resource('/mposplot')
class MPositionPlot(Resource):
    def get(self):
        span_length = request.args.get('spanLength', 'error', type=float)
        x_loc = request.args.get('xLoc', 'error', type=float)
        feet_or_frac = request.args.get('feetOrFrac', 'feet', type=str)
        max_moment_loc = request.args.get('maxMomentLoc', 'error', type=float)
        results = mvb.show_plot_moment(span_length, x_loc, feet_or_frac,\
                                       max_moment_loc)
        return jsonify(results)


@eng_api.resource('/vposplot')
class VPositionPlot(Resource):
    def get(self):
        span_length = request.args.get('spanLength', 'error', type=float)
        x_loc = request.args.get('xLoc', 'error', type=float)
        feet_or_frac = request.args.get('feetOrFrac', 'feet', type=str)
        max_shear_loc = request.args.get('maxShearLoc', 'error', type=float)
        results = mvb.show_plot_shear(span_length, x_loc, feet_or_frac,\
                                       max_shear_loc)
        return jsonify(results)


@eng_api.resource('/mplot')
class MPlot(Resource):
    def get(self):
        span_length = request.args.get('spanLength', 'error', type=float)
        num_points = request.args.get('numPoints', 'error', type=int)
        incr = request.args.get('increment', 'error', type=float)
        impact_factor = request.args.get('impactFactor', 'error', type=float)
        dist_factor = request.args.get('distFactor', 'error', type=float)
        results = mvb.nth_point_moment(span_length, num_points, incr,
                                impact_factor, dist_factor)
        return jsonify(results)


@eng_api.resource('/vplot')
class VPlot(Resource):
    def get(self):
        span_length = request.args.get('spanLength', 'error', type=float)
        num_points = request.args.get('numPoints', 'error', type=int)
        incr = request.args.get('increment', 'error', type=float)
        impact_factor = request.args.get('impactFactor', 'error', type=float)
        dist_factor = request.args.get('distFactor', 'error', type=float)
        results = mvb.nth_point_shear(span_length, num_points, incr,
                                impact_factor, dist_factor)
        return jsonify(results)


@eng_api.resource('/vreact')
class VReact(Resource):
    def get(self):
        span_length_1 = request.args.get('spanLength1', 'error', type=float)
        span_length_2 = request.args.get('spanLength2', 'error', type=float)
        incr = request.args.get('increment', 'error', type=float)
        impact_factor = request.args.get('impactFactor', 'error', type=float)
        dist_factor = request.args.get('distFactor', 'error', type=float)
        results = mvb.max_pier_reaction(span_length_1, span_length_2, incr,\
                                    impact_factor, dist_factor)
        return jsonify(results)


@eng_api.resource('/beam')
class Beam(Resource):
    def post(self):
        data = request.get_json()
        results = beam.main(data)
        def_shape_vals = deflected_shape.main(results['d'])
        return jsonify({'results':results, 'def':def_shape_vals})
