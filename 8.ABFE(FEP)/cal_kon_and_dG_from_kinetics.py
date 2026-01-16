import numpy as np

def cal_t_with_error(k_on, L, se_k_on):

    if k_on is None or se_k_on is None:
        return None, None
    
    t = 1/(4 * k_on * L)
    se_t = se_k_on/(4 * k_on**2 * L)
    return t, se_t


def calculate_kon(n0, n_single, n_double, t_single, t_double, t_double_prime, T, L):
    """
    Parameters:
    - n0: Number of simulations without binding
    - n_single: Number of simulations with one binding event
    - n_double: Number of simulations with two binding events
    - t_single: Binding time for simulations with one binding event
    - t_double: First binding time for simulations with two binding events
    - t_double_prime: Second binding time for simulations with two binding events
    - T: Total simulation time
    - L: Ligand concentration

    Returns:
    - k_on: Binding rate constant
    """
    term1 = -4 * L * T * n0

    term2 = -np.sum(4 * L * t_single + 3 * L * (T - t_single)) if np.sum(t_single) > 0 else 0

    term3 = -np.sum(4 * L * t_double + 
                    3 * L * (t_double_prime - t_double) + 
                    2 * L * (T - t_double_prime)) if np.sum(t_double) > 0 else 0
    C = term1 + term2 + term3
    k_on = -(n_single + 2 * n_double) / C

    se_k_on = np.sqrt(n_single + 2 * n_double)/abs(C)
    
    return k_on, se_k_on

if __name__ == "__main__":
    EOL = {
        'n0': np.float64(8),  
        'n_single': np.float64(2),
        'n_double': np.float64(0),
        't_single': np.array([0.000000637,0.000000860], dtype=np.float64),
        't_double': np.array([0]),
        't_double_prime': np.array([0]),
        'T': np.float64(0.000001), 
        'L': np.float64(0.0096)     
    }

    EOL_k_on_est, EOL_se_k_on = calculate_kon(
        EOL['n0'], 
        EOL['n_single'],
        EOL['n_double'],
        EOL['t_single'],
        EOL['t_double'],
        EOL['t_double_prime'],
        EOL['T'],
        EOL['L']
    )

    print(f"k_on of EOL: {EOL_k_on_est} M^-1 s^-1 ± {EOL_se_k_on} M^-1 s^-1")
    EOL_t, EOL_se_t = cal_t_with_error(EOL_k_on_est, EOL['L'], EOL_se_k_on)
    print(f"ton of EOL: {EOL_t} s ± {EOL_se_t} s")

    DEET = {
        'n0': np.float64(6),  
        'n_single': np.float64(2),  
        'n_double': np.float64(2),  
        't_single': np.array([0.00000077,0.000000976], dtype=np.float64), 
        't_double': np.array([0.000000400,0.00000054], dtype=np.float64),      
        't_double_prime': np.array([0.000000980,0.000000950], dtype=np.float64),                
        'T': np.float64(0.000001), 
        'L': np.float64(0.0096) 
    }

    DEET_k_on_est, DEET_se_k_on = calculate_kon(
        DEET['n0'], 
        DEET['n_single'],
        DEET['n_double'],
        DEET['t_single'],
        DEET['t_double'],
        DEET['t_double_prime'],
        DEET['T'],
        DEET['L']
    )
    DEET_t, DEET_se_t = cal_t_with_error(DEET_k_on_est, DEET['L'], DEET_se_k_on)
    print(f"k_on of DEET: {DEET_k_on_est} M^-1 s^-1 ± {DEET_se_k_on} M^-1 s^-1")
    print(f"ton of DEET: {DEET_t} s ± {DEET_se_t} s")

    EOL_koff = 5.04
    EOL_koff_se = 2.37
    kb =8.314462618
    T = 310

    EOL_kd = EOL_koff/EOL_k_on_est
    EOL_kd_se = EOL_kd * np.sqrt((EOL_koff_se/EOL_koff)**2 + (EOL_se_k_on/EOL_k_on_est)**2)
    dG_EOL = kb*T*np.log(EOL_kd)
    dG_EOL_se = kb*T*EOL_kd_se/EOL_kd
    print(f"kd of EOL: {EOL_kd} M ± {EOL_kd_se} M")
    print(f"dG of EOL: {dG_EOL/(4.184*1000)} kcal/M ± {dG_EOL_se/(4.184*1000)} kcal/M")

    DEET_koff = 0.018
    DEET_koff_se = 0.006
    kb =8.314462618
    T = 310

    DEET_kd = DEET_koff/DEET_k_on_est
    DEET_kd_se = DEET_kd * np.sqrt((DEET_koff_se/DEET_koff)**2 + (DEET_se_k_on/DEET_k_on_est)**2)
    dG_DEET = kb*T*np.log(DEET_kd)
    dG_DEET_se = kb*T*DEET_kd_se/DEET_kd
    print(f"kd of DEET: {DEET_kd} M ± {DEET_kd_se} M")
    print(f"dG of DEET:  {dG_DEET/(4.184*1000)} kcal/M ± {dG_DEET_se/(4.184*1000)} kcal/M")

    DEET_koff_mle = 0.010
    DEET_koff_se_mle = 0.0037
    kb =8.314462618
    T = 310

    DEET_kd_mle = DEET_koff_mle/DEET_k_on_est
    DEET_kd_se_mle = DEET_kd_mle * np.sqrt((DEET_koff_se_mle/DEET_koff_mle)**2 + (DEET_se_k_on/DEET_k_on_est)**2)
    dG_DEET_mle = kb*T*np.log(DEET_kd_mle)
    dG_DEET_se_mle = kb*T*DEET_kd_se_mle/DEET_kd_mle
    print(f"kd of DEET mle: {DEET_kd_mle} M ± {DEET_kd_se_mle} M")
    print(f"dG of DEET mle:  {dG_DEET_mle/(4.184*1000)} kcal/M ± {dG_DEET_se_mle/(4.184*1000)} kcal/M")
