theory GodelNetAddCausalityAuditFull
  imports GodelNetAddRivalRule
begin

text \<open>
  This separate theory deliberately imports the rival theorem's ambient
  context. It is not imported by the core-only ablation audit.
\<close>

lemma audit_rival_context_ifo_alone_is_inconsistent:
  assumes "in_force_omsp t2"
  shows False
  using assms in_force_omsp_false_t2 by blast

lemma audit_rival_context_ifo_entails_anything:
  assumes "in_force_omsp t2"
  shows "\<psi>"
  using audit_rival_context_ifo_alone_is_inconsistent[OF assms] by blast

text \<open>
  Removing the forbidden-case assumption is a different test. The strong
  rule is added only as a probe hypothesis, not as a theory axiom.
\<close>

lemma audit_full_unguarded_rule_consistency:
  assumes "\<forall>\<phi> t. attempted \<phi> t \<and> is_amd \<phi> t \<and>
    (\<forall>g. is_leg g t \<longrightarrow> sup_prop g \<phi> t) \<longrightarrow> is_prop \<phi> t"
  shows False
  nitpick[user_axioms, card time = 4, show_consts, timeout = 300] oops

end
