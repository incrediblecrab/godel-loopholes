(* ------------------------------------------------------------------------
   Countermodel.thy

   Semantic negative controls for GodelConstitution.thy.

   The model itself is NOT restated here. It is imported, so there is exactly
   one copy of the transcription in this repository and a correction to it
   cannot fail to reach this file.
   ------------------------------------------------------------------------ *)

theory Countermodel
  imports GodelConstitution
begin

(* -------- SEMANTIC NEGATIVE CONTROLS (countermodel search) --------
   A failed tactic only shows that one tactic failed. Nitpick is a model
   finder: if it returns a countermodel that respects the user axioms, the
   goal is genuinely NOT entailed by the axiom set. Each goal below is the
   dual of a theorem proved in GodelConstitution.thy, so each MUST yield a
   countermodel.
   ------------------------------------------------------------------ *)

lemma NEG1_dictatorship_at_t1: "\<lfloor>Dictatorship\<rfloor>t1"
  nitpick[user_axioms, card time = 4, timeout = 180] oops

lemma NEG2_dictatorship_at_t2: "\<lfloor>Dictatorship\<rfloor>t2"
  nitpick[user_axioms, card time = 4, timeout = 180] oops

lemma NEG3_no_dictatorship_at_t3: "\<lfloor>\<^bold>\<not> Dictatorship\<rfloor>t3"
  nitpick[user_axioms, card time = 4, timeout = 180] oops

end
