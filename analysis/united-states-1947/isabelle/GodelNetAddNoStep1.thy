(* ------------------------------------------------------------------------
   GodelNetAddNoStep1.thy

   The ablation: GodelNetAddCore WITHOUT step-one axioms.

   GodelNetAddCore contains the infrastructure, global rules, government,
   and step-two stipulations. This file imports it and adds NOTHING about
   step one. The entrenchment clause is in force at t1 (axiom in Core) and
   no repeal is asserted. This does not assert that no repeal occurs or
   that the clause persists without one.

   THE QUESTION: is Dictatorship_t3 still entailed?

   A countermodel to Dictatorship_t3 shows that deleting the step-one
   package removes entailment. It does not show causal necessity or that
   each individual fact is indispensable.

   If Nitpick also finds a countermodel to NOT Dictatorship_t3, then the
   theorem is INDEPENDENT without step one (neither provable nor refutable),
   which is the expected result: Core does not fix in_force_omsp at t2,
   and comsp blocks amd2 only when it is true. Blocking that amendment
   does not itself block the dictatorship predicate; frames are absent.

   EVERY PROBE HERE IS DIAGNOSTIC, NOT PROOF. Nitpick is a bounded model
   finder; a countermodel is a genuine negative, but failure to find one is
   inconclusive, not a positive answer.
   ------------------------------------------------------------------------ *)

theory GodelNetAddNoStep1
  imports GodelNetAddCore
begin

(* No step-one axioms are added here. Compare GodelNetAddFull.thy, which
   adds five axioms about amd1a. *)

(* ===== MANDATORY CONSISTENCY PROBE =====
   A countermodel to False explicitly checks the reduced theory's
   consistency. A genuine countermodel to any other conjecture would
   also witness consistency of its ambient axioms. *)

lemma no_step1_consistent: "False"
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

(* ===== THE RESULT: DOES STEP ONE DO WORK? =====
   A countermodel here means Dictatorship_t3 is NOT entailed without step
   one. The expected countermodel has in_force_omsp true at t2, so comsp
   blocks the dictatorship amendment from being validly proposed. *)

lemma dictatorship_without_step1: "\<lfloor>Dictatorship\<rfloor>t3"
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

(* ===== DUAL: independence, not refutation =====
   A countermodel here confirms that NOT Dictatorship_t3 is also not
   entailed, so the theorem is independent without step one: the model
   does not determine Dictatorship_t3. See GodelNetAddCausalityAudit for
   the stronger no-ratification and clause-always-on countermodels. *)

lemma no_dictatorship_without_step1: "\<lfloor>\<^bold>\<not> Dictatorship\<rfloor>t3"
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

end
