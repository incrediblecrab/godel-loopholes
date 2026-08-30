(* ------------------------------------------------------------------------
   GodelNetAddFull.thy

   The full two-step argument with all three Z&B defects repaired.

   Imports GodelNetAddCore (infrastructure, rules, step-two stipulations)
   and adds the STEP-ONE axioms: the repeal amendment is attempted, is an
   amendment, has Congressional support, maintains Senate suffrage, and has
   ratification support from the states.

   THE KEY RESULT: amd2_proposed_t2 is DERIVED here, not assumed. The
   derivation chain is:

     1. pvr fires at t1: amd1a is validly proposed (it maintains suffrage,
        so the entrenchment clause does not block it)
     2. psr fires at t1: proposed + supported -> ratified at t2
     3. rv fires at t2: ratified amd1a -> amd1a holds -> NOT in_force_omsp
     4. pvr fires at t2: amd2 is validly proposed (the entrenchment clause
        is no longer in force, so the suffrage check is vacuously passed)
     5. psr fires at t2: proposed + supported -> ratified at t3
     6. rv fires at t3: ratified amd2 -> Dictatorship

   Every theorem and consistency probe in this file is machine-checked.
   ------------------------------------------------------------------------ *)

theory GodelNetAddFull
  imports GodelNetAddCore
begin

(* ===== STEP-ONE AXIOMS =====

   Five stipulations about the repeal amendment:
   - It is attempted (put forward for proposal)
   - It is an amendment
   - Congress supports it
   - It maintains Senate suffrage (the repeal of the entrenchment clause
     does not itself change Senate representation)
   - The states support ratification *)

axiomatization where
  amd1a_attempted_t1:   "\<lfloor>attempted amd1a\<rfloor>t1" and
  is_amd_amd1a_t1:      "\<lfloor>is_amd amd1a\<rfloor>t1" and
  sup_prop_amd1a_t1:    "\<lfloor>sup_prop Congress amd1a\<rfloor>t1" and
  maint_suf_amd1a_t1:   "\<lfloor>maint_suf amd1a\<rfloor>t1" and
  amd1a_sup_rat_t1:     "\<lfloor>sup_rat amd1a\<rfloor>t1"

(* ===== DERIVATION CHAIN ===== *)

(* Step 1: amd1a is VALIDLY PROPOSED at t1.
   pvr fires because: attempted, is_amd, Congress supports, and the
   entrenchment clause allows it (maint_suf amd1a holds). *)
lemma amd1a_proposed_t1: "\<lfloor>is_prop amd1a\<rfloor>t1"
proof -
  have "\<forall>g. is_leg g t1 \<longrightarrow> sup_prop g amd1a t1"
    using Con_Leg_t1 sup_prop_amd1a_t1 unique_is_leg
    unfolding Defs by blast
  thus ?thesis
    using amd1a_attempted_t1 is_amd_amd1a_t1 maint_suf_amd1a_t1 pvr_elim
    by (auto simp: local_valid_def)
qed

(* Step 2: amd1a is RATIFIED at t2.
   psr: proposed AND supported at t1 -> ratified at t2 (the successor of t1). *)
lemma amd1a_ratified_t2: "\<lfloor>is_rat amd1a\<rfloor>t2"
proof -
  have "\<lfloor>\<^bold>X(is_rat amd1a)\<rfloor>t1"
    using amd1a_proposed_t1 amd1a_sup_rat_t1 psr_global
    by (auto simp: global_valid_def local_valid_def tallB_s_def tall_s_def
                   tand_def timp_def tnext_def)
  thus ?thesis
    using t1_s_t2 by (auto simp: local_valid_def tnext_def)
qed

(* Step 3: amd1a TAKES EFFECT at t2.
   rv: ratified -> content holds. amd1a's content is NOT in_force_omsp.
   So the entrenchment clause is no longer in force at t2. *)
lemma amd1a_val_t2: "\<lfloor>amd1a\<rfloor>t2"
  using amd1a_ratified_t2 rv_global
  by (auto simp: global_valid_def local_valid_def tallB_s_def tall_s_def
                 timp_def)

lemma in_force_omsp_false_t2: "\<not>(in_force_omsp t2)"
  using amd1a_val_t2
  by (simp add: local_valid_def amd1a_def tneg_def)

(* Step 4: amd2 is VALIDLY PROPOSED at t2.
   THIS IS THE KEY DERIVED FACT. In Z&B it is the axiom amd2_prop_t2.
   pvr fires because: attempted, is_amd, Congress supports, and the
   entrenchment clause is NOT in force (from step 3), so the suffrage
   check is vacuously satisfied. *)
lemma amd2_proposed_t2: "\<lfloor>is_prop amd2\<rfloor>t2"
proof -
  have "\<forall>g. is_leg g t2 \<longrightarrow> sup_prop g amd2 t2"
    using Con_Leg_t2 sup_prop_amd2_t2 unique_is_leg
    unfolding Defs by blast
  thus ?thesis
    using amd2_attempted_t2 is_amd_amd2_t2 in_force_omsp_false_t2 pvr_elim
    by (auto simp: local_valid_def)
qed

(* Step 5: amd2 is ratified at t3 and takes effect. *)
lemma amd2_val_t3: "\<lfloor>amd2\<rfloor>t3"
proof -
  have "\<lfloor>\<^bold>X(is_rat amd2)\<rfloor>t2"
    using amd2_proposed_t2 amd2_sup_rat_t2 psr_global
    by (auto simp: global_valid_def local_valid_def tallB_s_def tall_s_def
                   tand_def timp_def tnext_def)
  thus ?thesis
    using rv_global t2_s_t3
    by (auto simp: global_valid_def local_valid_def tallB_s_def tall_s_def
                   timp_def tnext_def)
qed

(* Step 6: Dictatorship at t3. *)
theorem Dictatorship_t3: "\<lfloor>Dictatorship\<rfloor>t3"
proof -
  have "\<lfloor>is_leg P \<^bold>\<and> is_exe P \<^bold>\<and> is_jud P\<rfloor>t3"
    using amd2_val_t3 amd2_def
    by (simp add: local_valid_def tand_def)
  thus "\<lfloor>Dictatorship\<rfloor>t3"
    by (meson Dictatorship_def local_valid_def)
qed

(* ===== MANDATORY CONSISTENCY PROBES =====

   An inconsistent theory proves every formula including Dictatorship_t3.
   Both probes must succeed for the theorems above to carry information. *)

lemma full_model_satisfiable: "True"
  nitpick[satisfy, user_axioms, card time = 4, timeout = 300] oops

lemma full_model_consistent: "False"
  nitpick[user_axioms, card time = 4, timeout = 300] oops

end
