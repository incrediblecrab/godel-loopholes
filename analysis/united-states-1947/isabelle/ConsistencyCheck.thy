(* ------------------------------------------------------------------------
   ConsistencyCheck.thy

   Consistency controls for GodelConstitution.thy.

   The model itself is NOT restated here. It is imported, so there is exactly
   one copy of the transcription in this repository and a correction to it
   cannot fail to reach this file.
   ------------------------------------------------------------------------ *)

theory ConsistencyCheck
  imports GodelConstitution
begin

(* ---------------- CONSISTENCY CHECK ----------------
   Everything in GodelConstitution.thy is vacuous if the axiom set is
   inconsistent, because an inconsistent theory proves every formula including
   Dictatorship_t3. The thesis checks this with Nitpick at each time instance;
   this is the t3 check, which subsumes the earlier ones since axioms are only
   ever added.

   Two independent tests:
     1. Nitpick must FIND a satisfying model that respects the user axioms.
     2. Nitpick must FAIL to find a counterexample-free proof of False, i.e.
        an attempt to prove False must not succeed.
   ------------------------------------------------------------------ *)

lemma T_basic_sat_t3: "True"
  nitpick[satisfy, user_axioms, show_all, format = 2, card time = 4, timeout = 300] oops

lemma consistency_False: "False"
  nitpick[user_axioms, card time = 4, timeout = 300] oops

end
