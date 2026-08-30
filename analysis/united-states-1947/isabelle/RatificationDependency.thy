(* ------------------------------------------------------------------------
   RatificationDependency.thy

   The experiment this repository adds to Zahoransky & Benzmueller.

   THE CONTROL is GodelConstitution.thy, which is their model entire and which
   proves Dictatorship_t3.

   THE MANIPULATION is here. This theory loads the identical model from
   GodelCore.thy and adds back TWO of the three ratification-support axioms:

       amd1a_sup_rat_t1   assumed here
       amd1b_sup_rat_t1   assumed here
       amd2_sup_rat_t2    NOT ASSUMED

   amd2_sup_rat_t2 asserts that the amendment vesting legislative, executive
   and judicial power in one person "has support for ratification". It is the
   only thing withdrawn.

   WHAT sup_rat MEANS, STATED CAREFULLY
   It is an uninterpreted predicate. The thesis says so in section 4.1: "What
   this support looks like shall not be specified further." The same section
   lists three fourths of the State Legislatures and three fourths of State
   Conventions among the things it "shall not represent", on the ground that
   they "are part of the federal system which is not essential to the
   argument". So sup_rat is NOT "36 legislatures voted yes". It is the
   unanalysed condition that stands where Article V's ratification stage
   would go, and Article V permits either mode of ratification at Congress's
   direction. See ../ratification-price.md.

   WHAT A COUNTERMODEL TO NEG1 MEANS
   Nitpick is a model finder. A model in which every remaining axiom holds and
   Dictatorship is false at t3 shows that no proof of Dictatorship_t3 exists
   from the remaining axioms -- not merely that the authors' chosen proof used
   this one. That is the result, and it is the only one of the six below that
   is not already forced by the control being satisfiable.

   WHAT IT DOES NOT MEAN
   It does not show a dictatorship is impossible. NEG2 tests the dual and is
   expected to yield a countermodel too -- but see the note above NEG2: that
   outcome is a logical consequence of the control being satisfiable, so it
   confirms the setup rather than adding anything.

   Vantage: United States, December 5, 1947. 48 states, so Article V's three
   fourths is 36. The model contains no number anywhere; ../threshold-
   arithmetic.md derives the missing one.
   ------------------------------------------------------------------------ *)

theory RatificationDependency
  imports GodelCore
begin

(* The authors' step one: the two amendments that rewrite Article V have
   support for ratification. Granted here in full. This does NOT by itself put
   the model into its post-amendment state -- see the recorded null result
   below, which shows amd1a holds at t2 with no ratification axiom whatever. *)
axiomatization where
  amd1a_sup_rat_t1: "\<lfloor>sup_rat amd1a\<rfloor>t1" and
  amd1b_sup_rat_t1: "\<lfloor>sup_rat amd1b\<rfloor>t1"

(* amd2_sup_rat_t2 is deliberately absent. Nothing else is changed. *)

(* ---- A CHECK THAT DOES NOT WORK, RECORDED BECAUSE IT LOOKS LIKE IT DOES ----

   The obvious way to confirm that the reduced arm still has Article V amended
   is to prove amd1a at t2. It proves. It is also worthless as a check, because
   it proves without any ratification axiom at all: amd1a is the existential
   "some proposed amendment fails to maintain Senate suffrage", and GodelCore
   already asserts amd2_prop_t2 and amd2_not_maint_suf_t2, so amd2 witnesses it
   directly. The proof below deliberately cites no sup_rat axiom, to make the
   point unmissable.

   What actually puts the model into its post-amendment state is the omission
   of X omsp at t1, which is hard-coded in GodelCore and is the authors' own
   acknowledged concession. Nothing in this file changes it, and nothing in
   this file needs to. *)
lemma amd1a_valid_t2_without_any_ratification_axiom: "\<lfloor>amd1a\<rfloor>t2"
proof -
  have "\<not> maint_suf amd2 t2 \<and> is_prop amd2 t2"
    using amd2_prop_t2 amd2_not_maint_suf_t2
    by (simp add: local_valid_def tneg_def)
  thus ?thesis
    by (auto simp: local_valid_def amd1a_def texiB_s_def texi_s_def tand_def tneg_def)
qed

(* ---- CONSISTENCY. Without this the countermodels below mean nothing. ----

   HONEST NOTE ON WHAT THESE ADD. The control (GodelConstitution) is satisfiable
   and entails Dictatorship at t3. Write T for the reduced theory here and A for
   the withdrawn axiom. Since T is a subset of T + A, any model of T + A is a
   model of T. That single observation already forces FIVE of the six results
   in this file WITHOUT running anything:

     - T is satisfiable                        (reduced_model_is_satisfiable)
     - T does not entail False                 (reduced_model_not_trivial)
     - T does not entail the absence of D      (NEG2)
     - T does not entail A                     (FREE1, and see its note)
     - T does not entail not A                 (FREE2)

   because a model of T + A witnesses all of them. Only the countermodel to
   Dictatorship itself is new information. The forced checks are kept anyway,
   but as instrument checks: if Nitpick ever contradicted them, the tooling
   would be wrong, not the constitution. They are not findings. *)
lemma reduced_model_is_satisfiable: "True"
  nitpick[satisfy, user_axioms, card time = 4, timeout = 300] oops

lemma reduced_model_not_trivial: "False"
  nitpick[user_axioms, card time = 4, timeout = 300] oops

(* ---- THE RESULT. This one is not forced by the control. ----
   A countermodel here says no proof of Dictatorship_t3 exists from the
   remaining axioms, which is strictly more than observing that the authors'
   proof happened to cite amd2_sup_rat_t2. *)
lemma NEG1_dictatorship_not_entailed: "\<lfloor>Dictatorship\<rfloor>t3"
  nitpick[user_axioms, card time = 4, timeout = 300] oops

(* ---- THE DUAL, WHICH IS FORCED. Kept as a guard against misreading NEG1
   as a safety result, not as a finding in its own right. ---- *)
lemma NEG2_absence_not_entailed_either: "\<lfloor>\<^bold>\<not> Dictatorship\<rfloor>t3"
  nitpick[user_axioms, card time = 4, timeout = 300] oops

(* ---- WHY NEG1 IS NOT JUST A DEPENDENCY LIST ----

   Reading GodelConstitution shows that the authors' proof of Dictatorship_t3
   cites amd2_sup_rat_t2. That is visible in the thesis too. NEG1 says more:
   no proof exists from the remaining axioms, by any route. That is the whole
   of the contribution, and the two lemmas below do NOT add to it.

   THE TWO BELOW ARE FORCED. Writing T for this theory, A for the withdrawn
   axiom and D for dictatorship at t3:
     FREE1  if T |= A then T |= D, contradicting NEG1; so T |/= A. Indeed any
            NEG1 countermodel must already falsify A.
     FREE2  a model of T + A is a model of T satisfying A, so T |/= not A.
   They are kept as instrument checks only. They locate nothing. An earlier
   version of this file presented them as independent evidence that the model
   holds no information about ratification, which was wrong twice over: they
   are corollaries, and underdetermination does not measure how richly a
   theory represents something in any case.

   AND THE SYNTACTIC ARGUMENT FOR THEM WAS ALSO WRONG. It ran: sup_rat only
   ever appears in the antecedent of osr and psr, so no axiom can conclude it,
   so it can only be stipulated. That is invalid in classical logic, and the
   lemma below is the refutation. osr is (not S) --> (not R), whose
   contrapositive is R --> S. Given ratification, support follows. The lemma
   is stated with an explicit hypothesis rather than an axiom so that it
   cannot contaminate the experiment above. *)

lemma sup_rat_IS_derivable_from_ratification:
  assumes "\<lfloor>\<^bold>X(is_rat amd2)\<rfloor>t2"
  shows   "\<lfloor>sup_rat amd2\<rfloor>t2"
  using assms osr_t2
  by (auto simp: local_valid_def tallB_s_def tall_s_def tallB_g_def tall_g_def
                 timp_def tneg_def tnext_def)

lemma FREE1_support_not_entailed: "\<lfloor>sup_rat amd2\<rfloor>t2"
  nitpick[user_axioms, card time = 4, timeout = 300] oops

lemma FREE2_absence_of_support_not_entailed: "\<lfloor>\<^bold>\<not> (sup_rat amd2)\<rfloor>t2"
  nitpick[user_axioms, card time = 4, timeout = 300] oops

end
