// usage: 
//javac -cp stanford-corenlp-full-2016-10-31/*:.  CorefReplacer.java 
//java -cp stanford-corenlp-full-2016-10-31/*:.  CorefReplacer
import java.util.*;

import edu.stanford.nlp.coref.CorefCoreAnnotations;
import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.coref.data.Mention;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class CorefReplacer {
  public static void main(String[] args) throws Exception {
    String text = "John drove to Judy’s house. He made her dinner. She sucked his lollipop.";
    Annotation doc = new Annotation(text);
    Properties props = new Properties();
    props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,mention,coref");
    StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
    pipeline.annotate(doc);


    Map<Integer, CorefChain> corefs = doc.get(CorefCoreAnnotations.CorefChainAnnotation.class);
    List<CoreMap> sentences = doc.get(CoreAnnotations.SentencesAnnotation.class);


    List<String> resolved = new ArrayList<String>();

    for (CoreMap sentence : sentences) {

      List<CoreLabel> tokens = sentence.get(CoreAnnotations.TokensAnnotation.class);

      for (CoreLabel token : tokens) {

        Integer corefClustId= token.get(CorefCoreAnnotations.CorefClusterIdAnnotation.class);
        CorefChain chain = corefs.get(corefClustId);


        if (chain==null || chain.getMentionsInTextualOrder().size() == 1) {
          resolved.add(token.word());
        }else{

          int sentINdx = chain.getRepresentativeMention().sentNum -1;
          CoreMap corefSentence = sentences.get(sentINdx);
          List<CoreLabel> corefSentenceTokens = corefSentence.get(CoreAnnotations.TokensAnnotation.class);

          String newwords = "";
          CorefChain.CorefMention reprMent = chain.getRepresentativeMention();
          for(int i = reprMent.startIndex; i<reprMent.endIndex; i++){
                    CoreLabel matchedLabel = corefSentenceTokens.get(i-1); //resolved.add(tokens.get(i).word());
                    resolved.add(matchedLabel.word());

                    newwords+=matchedLabel.word()+" ";

          }

          //System.out.println("converting " + token.word() + " to " + newwords);
        }
      }

    }


    String resolvedStr ="";
    System.out.println();
    for (String str : resolved) {
      if (str.equals("'s")) // avoid double 's 's problem
        continue;
      resolvedStr+=str+" ";
    }
    System.out.println(resolvedStr);
  }
}
