import numpy as np

def heuristic_attack(S, x, p, t, k):    
    sorted_inds = np.argsort(-x)
        
    S_bar = S[sorted_inds,:]
    x_bar = x[sorted_inds]
            
    for rho in range(S.shape[0]):

        x_srho = x_bar[rho]
        
        p_p = x_srho
        S_pp = [S_bar[rho,:]]
        
        rho_p = rho + 1
        
        while p_p <= 1-p and rho_p < S.shape[0]:
            
            x_srho_p = x_bar[rho_p]
            
            p_p += x_srho_p
            S_pp.append(S_bar[rho_p,:])
            
            rho_p += 1
        
        if p_p > 1-p:    
        #if p_p > p: 
            
            S_pp_any = np.any(S_pp, axis=0)
            
            t_sorted_inds = np.argsort(t)
            t_sorted = t[t_sorted_inds]
            
            S_pp_any_sorted = S_pp_any[t_sorted_inds]
            
            inds_to_delete = []
            for i in range(t_sorted.shape[0]):
                s_i = S_pp_any_sorted[i]
                if not s_i:
                    inds_to_delete.append(i)
                if len(inds_to_delete) == k:
                    break

            t_sorted[inds_to_delete] = 0
            if np.sum(t_sorted) > 0:
                original_inds = t_sorted_inds[inds_to_delete]
                
                a = np.zeros(S.shape[1])
                a[original_inds] = 1
                return a
                
    return None
                
                
                
                