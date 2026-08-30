(* ------------------------------------------------------------------------
   GodelConstitution.thy

   Replication of:
     Valeria Zahoransky, "Modelling the US Constitution in HOL", BSc thesis,
     Freie Universitaet Berlin, 2019 (supervisor: Christoph Benzmueller), and
     Zahoransky & Benzmueller, "Modelling the US Constitution to establish
     constitutional dictatorship", MIREL 2019 @ JURIX, CEUR vol. 2632.

   The authors publish no .thy file. This theory is transcribed by hand from
   the thesis PDF, sections 4.2 and 4.3. Section numbers in the comments below
   refer to the thesis.

   The argument being formalised is Guerra-Pujol's reconstruction of Goedel's
   claim, NOT Goedel's own reasoning, which survives in no source. The authors
   state this themselves in their second paragraph.

   Replication targets, in order:
     theorem noDictatorship_t1   -- no dictatorship under the 1947 Constitution
     theorem noDictatorship_t2   -- none after Article V is amended
     theorem Dictatorship_t3     -- dictatorship, by lawful steps only

   SPLIT NOTE. This transcription is divided across two files:
     GodelCore.thy          everything not depending on a sup_rat axiom
     GodelConstitution.thy  the three sup_rat axioms and what they carry
   The union is the thesis model, axiom for axiom. The split exists so that
   RatificationDependency.thy can load the model WITHOUT assuming the states
   ratify. Regrouping axioms into different blocks does not change the theory.

   ------------------------------------------------------------------------ *)

theory GodelConstitution
  imports GodelCore
begin

(* The three axioms that ASSERT ratification support. sup_rat is uninterpreted:
   the thesis states at 4.1 that "what this support looks like shall not be
   specified further", and lists three fourths of the State Legislatures and
   three fourths of State Conventions among the things it will not represent,
   as "not essential to the argument". So each of these axioms is one bit
   standing where Article V's ratification stage would go. What that bit is
   worth is examined in ../ratification-price.md; ../search/quorum_cascade.py
   handles the separate proposing stage. *)
axiomatization where
  amd1a_sup_rat_t1: "\<lfloor>sup_rat amd1a\<rfloor>t1" and
  amd1b_sup_rat_t1: "\<lfloor>sup_rat amd1b\<rfloor>t1" and
  amd2_sup_rat_t2:  "\<lfloor>sup_rat amd2\<rfloor>t2"

lemma amd1a_val_t2: "\<lfloor>amd1a\<rfloor>t2"
proof -
  have "\<lfloor>\<^bold>X(is_rat amd1a)\<rfloor>t1"
    using amd1a_prop_t1 amd1a_sup_rat_t1 psr_t1 local_valid_def tallB_s_def
          tall_s_def tand_def timp_def tnext_def
    by auto
  thus "\<lfloor>amd1a\<rfloor>t2"
    using local_valid_def tallB_s_def tall_s_def timp_def tnext_def rv_t2 t1_s_t2
    by auto
qed

lemma amd1b_val_t2_2: "\<lfloor>amd1b\<rfloor>t2"
  unfolding Defs using amd1b_sup_rat_t1 amd1b_prop_t1 psr_t1 rv_t2
  by (simp add: amd1b_def tallB_s_def tall_s_def timp_def tneg_def tor_def)

lemma amd2_val_t3: "\<lfloor>amd2\<rfloor>t3"
proof -
  have "\<lfloor>\<^bold>X(is_rat amd2)\<rfloor>t2"
    using amd2_prop_t2 amd2_sup_rat_t2 local_valid_def tallB_s_def tall_s_def
          tand_def timp_def tnext_def psr_t2
    by auto
  thus "\<lfloor>amd2\<rfloor>t3"
    using local_valid_def tallB_s_def tall_s_def timp_def tnext_def rv_t3 t2_s_t3
    by auto
qed

theorem Dictatorship_t3: "\<lfloor>Dictatorship\<rfloor>t3"
proof -
  have "\<lfloor>is_leg P \<^bold>\<and> is_exe P \<^bold>\<and> is_jud P\<rfloor>t3"
    using amd2_val_t3 amd2_def
    by (simp add: local_valid_def tand_def)
  thus "\<lfloor>Dictatorship\<rfloor>t3"
    by (meson Dictatorship_def local_valid_def)
qed

end
