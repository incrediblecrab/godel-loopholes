(* Adversarial evidence for `step-one-repair.md`.

   This is the original rival-rule experiment, not a proof that the repaired
   proposal rule is uniquely forced. Its proofs are preserved. See
   GodelNetAddCausalityAudit and GodelNetAddCausalityAuditFull for the isolated
   compatibility argument and the ambient-context audit.

   PROBE 1 (Nitpick, diagnostic). Runs the full theory with show_consts so the
   model can be inspected rather than merely counted. A theory satisfied only
   by a degenerate model says nothing.

   PROBE 2 (kernel proof). `rival_pvr_inconsistency` shows that a proposal rule
   dropping the entrenchment check -- attempted AND is_amd AND sup_prop implies
   is_prop -- contradicts `comsp`, the conditional entrenchment clause, whenever
   the clause is in force and the amendment does not maintain equal suffrage.
   The displayed reasoning is sound, but Full already entails that the clause
   is off at t2. The contrary clause-on hypothesis alone is inconsistent with
   this import; the rival rule is not needed for that ambient contradiction.
   Neither this theorem nor the ablation proves causal necessity. *)

theory GodelNetAddRivalRule
  imports GodelNetAddFull
begin

(* ===== PROBE 1: Full-model shape =====
   Nitpick with show_consts shows the actual model assignments. *)

lemma full_model_shape: "True"
  nitpick[satisfy, user_axioms, card time = 4, show_consts, timeout = 300] oops

(* ===== PROBE 2: Rival pvr without entrenchment check =====
   pvr_strong: attempted AND is_amd AND sup_prop -> is_prop
   No disjunction with in_force_omsp / maint_suf.
   The strong rule is a local hypothesis, not an added theory axiom.
   The forbidden trigger makes it conflict with comsp. The imported Full
   theory also independently excludes that trigger, so this is not an
   isolated consistency comparison or a uniqueness theorem for pvr. *)

lemma rival_pvr_inconsistency:
  assumes pvr_strong: "\<forall>\<phi> t. attempted \<phi> t \<and> is_amd \<phi> t \<and>
            (\<forall>g. is_leg g t \<longrightarrow> sup_prop g \<phi> t) \<longrightarrow> is_prop \<phi> t"
  assumes comsp_holds: "\<forall>\<phi> t. in_force_omsp t \<and> \<not> maint_suf \<phi> t \<longrightarrow> \<not> is_prop \<phi> t"
  assumes att: "attempted amd2 t2" and amd: "is_amd amd2 t2"
  assumes sup: "\<forall>g. is_leg g t2 \<longrightarrow> sup_prop g amd2 t2"
  assumes notsuf: "\<not> maint_suf amd2 t2"
  assumes ifo: "in_force_omsp t2"
  shows "False"
proof -
  from pvr_strong att amd sup have "is_prop amd2 t2" by blast
  moreover from comsp_holds ifo notsuf have "\<not> is_prop amd2 t2" by blast
  ultimately show False by contradiction
qed

end
