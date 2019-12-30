import itertools

def arc_revise(var1,var2,problem,constraints_for_variable):
    '''Implements REVISE procedure from AC1 algorithm'''

    domain1 = problem._variables[var1]
    ind_to_del = []
    domain_changed = False
    for ind1, a1 in enumerate(domain1):
        found = False
        domain_changed = False
        if var2 in constraints_for_variable:
            for a2 in problem._variables[var2]:
                if not found:
                    for constr in constraints_for_variable[var2]:
                        vars = tuple(constr[1])
                        if tuple(vars) == (var1, var2):
                            res = constr[0](constr[1], problem._variables, {vars[0]: a1, vars[1]: a2})
                            if res and not found:
                                found = True
                                break
                else:
                    break
        if not found:
            print ('Remove',domain1[ind1],'from domain',domain1,'for variable',var1)
            domain_changed = True
            ind_to_del.append(ind1)

    if ind_to_del:
        problem._variables[var1] = [domain1[idx] for idx,_ in enumerate(domain1) if idx not in ind_to_del]
    return domain_changed



def ac1(arcs, problem):
    '''Implements AC1 procedure'''
    domain_changed = True
    if arcs:
        while domain_changed:
            domain_changed = False
            for arc in arcs.items():
                var1 = arc[0]
                for arc_item in arc[1].items():
                    var2 = arc_item[0]
                    res = arc_revise(var1, var2,problem,arc[1])
                    domain_changed = res or domain_changed

def path_revise(var1, var2, var3,problem):
    '''Implements PATH_REVISE procedure from PC1 algorithm'''
    for idx, constraint in enumerate(problem._constraints):
        vars = constraint[1]
        if len(vars)==2 and tuple(vars)==(var1,var2):
            R_ij = constraint[0]
            for a1 in problem._variables[var1]:
                for a2 in problem._variables[var2]:
                    res = R_ij(vars, problem._variables, {vars[0]: a1, vars[1]: a2})
                    if res:
                        for a3 in problem._variables[var2]:
                            got_1k = False
                            got_2k = False
                            for r_k in problem._constraints:
                                got_1k = tuple(r_k[1])==(var1,var3) and r_k[0](r_k[1], problem._variables, {r_k[1][0]: a1, r_k[1][1]: a3})
                                got_2k = tuple(r_k[1])==(var2,var3) and r_k[0](r_k[1], problem._variables, {r_k[1][0]: a2, r_k[1][1]: a3})

                                if got_1k and got_2k:
                                    break
                            if got_1k and got_2k:
                                #print(f'{var1}={a1}, {var2}={a2}, {var3}={a3}, OK')
                                break
                        if not (got_1k and got_2k):

                            # Remove pair from constraint
                            new_constraint = lambda v1,v2: (v1,v2)!=(a1,a2) and constraint[0](constraint[1],problem._variables,{constraint[1][0]:a1,constraint[1][1]:a2})
                            variables = constraint[1]

                            # Remove old constraint
                            del problem._constraints[idx]

                            # Append updated constraint
                            problem.addConstraint(new_constraint,variables)
                            constraint = problem._constraints[-1]
                            print(f'Pair removed: ({var1}={a1},{var2}={a2})')
                            return True
    return False

def pc1(problem):
    '''Implements PC1 algorithm'''
    variables = problem._variables
    constraint_changed = True
    while constraint_changed:
        constraint_changed = False
        for triple in itertools.permutations(variables,3):
            constraint_changed = constraint_changed or path_revise(triple[0],triple[1],triple[2],problem)


