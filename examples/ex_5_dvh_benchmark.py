"""
    This example demonstrates the use of portpy to create down sampled influence matrix and
    optimize it with exact dvh constraints for benchmarking
"""
import portpy as pp


def ex_5_dvh_benchmark():
    # Enter patient name
    patient_id = 'Lung_Patient_1'

    # visualize patient metadata for beams_dict and structures
    pp.Visualize.display_patient_metadata(patient_id)

    # display patients
    pp.Visualize.display_patients()

    # create my_plan object for the planner beams_dict
    # for the customized beams_dict, you can pass the argument beam_ids
    # e.g. my_plan = Plan(patient_name, beam_ids=[0,1,2,3,4,5,6], options=options)
    my_plan = pp.Plan(patient_id)

    # create a influence matrix down sampled beamlets of width and height 5mm
    down_sample_factor = [5, 5, 1]
    opt_vox_xyz_res_mm = [ct_res * factor for ct_res, factor in zip(my_plan.get_ct_res_xyz_mm(), down_sample_factor)]
    inf_matrix_dbv = my_plan.create_inf_matrix(beamlet_width_mm=5, beamlet_height_mm=5, opt_vox_xyz_res_mm=opt_vox_xyz_res_mm)

    # run imrt fluence map optimization using cvxpy and one of the supported solvers and save the optimal solution in sol
    # CVXPy supports several opensource (ECOS, OSQP, SCS) and commercial solvers (e.g., MOSEK, GUROBI, CPLEX)
    # For optimization problems with non-linear objective and/or constraints, MOSEK often performs well
    # For mixed integer programs, GUROBI/CPLEX are good choices
    # If you have .edu email address, you can get free academic license for commercial solvers
    # we recommend the commercial solver MOSEK as your solver for the problems in this example,
    # however, if you don't have a license, you can try opensource/free solver SCS or ECOS
    # see https://www.cvxpy.org/tutorial/advanced/index.html for more info about CVXPy solvers
    # To set up mosek solver, you can get mosek license file using edu account and place the license file in directory C:\Users\username\mosek
    sol_no_dvh = pp.Optimize.run_IMRT_fluence_map_CVXPy(my_plan, inf_matrix=inf_matrix_dbv)

    # optimize with downscaled influence matrix and exact dvh constraint
    sol_dvh = pp.Optimize.run_IMRT_fluence_map_CVXPy_dvh_benchmark(my_plan, inf_matrix=inf_matrix_dbv)

    # Comment/Uncomment these lines to save & load plan and optimal solutions
    # my_plan.save_plan(path=r'C:\temp')
    # my_plan.save_optimal_sol(sol_no_dvh, sol_name='sol_no_dvh', path=r'C:\temp')
    # my_plan.save_optimal_sol(sol_dvh, sol_name='sol_dvh', path=r'C:\temp')
    # my_plan = Plan.load_plan(path=r'C:\temp')
    # sol_no_dvh = Plan.load_optimal_sol('sol_no_dvh', path=r'C:\temp')
    # sol_dvh = Plan.load_optimal_sol('sol_dvh', path=r'C:\temp')

    # plot fluence in 3d
    pp.Visualize.plot_fluence_3d(beam_id=0, sol=sol_no_dvh)
    pp.Visualize.plot_fluence_3d(beam_id=0, sol=sol_dvh)

    # plot fluence in 2d
    pp.Visualize.plot_fluence_2d(beam_id=0, sol=sol_no_dvh)
    pp.Visualize.plot_fluence_2d(beam_id=0, sol=sol_dvh)

    # plot dvh dvh for both the cases
    structs = ['PTV', 'ESOPHAGUS', 'HEART', 'CORD']

    pp.Visualize.plot_dvh(my_plan, sol=sol_no_dvh, structs=structs, style='solid', show=False)
    pp.Visualize.plot_dvh(my_plan, sol=sol_dvh, structs=structs, style='dotted', create_fig=False)

    # visualize 2d dose_1d for both the cases
    pp.Visualize.plot_2d_dose(my_plan, sol=sol_no_dvh)
    pp.Visualize.plot_2d_dose(my_plan, sol=sol_dvh)

    print('Done!')


if __name__ == "__main__":
    ex_5_dvh_benchmark()