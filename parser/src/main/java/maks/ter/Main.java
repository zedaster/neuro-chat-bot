package maks.ter;

import java.io.File;
import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

public class Main {
    public static void main(String[] args) {
        Document doc;
        try {
            //doc = Jsoup.connect("https://urfu.ru/ru/feedback/priem/obshchie-voprosy-po-priemu").get();
            doc = Jsoup.parse(new File("//home/grish-grdv/Pictures/Общие вопросы по приему.html"));
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }

        HashMap<String, String> questionAnswers = new HashMap<>();
        String prevQuestion = null;

        for (Element element: doc.body().getElementsByClass("urfu-feedback")) {

            for (Element div: element.children()) {

                if (prevQuestion == null && div.className().equals("question")) {
                    prevQuestion = div.text();
                    continue;
                }

                if (prevQuestion != null && div.className().equals("answer")) {
                    questionAnswers.put(prevQuestion, div.text());
                    prevQuestion = null;
                }
            }
        }

        questionAnswers.entrySet().forEach(data ->
            System.out.println(data.getKey() + ">>>>>>>>>>>>>: " + data.getValue())
        );

        String allQuestion = String.join(". ", questionAnswers.keySet());
        Map<String, Long> wordCount = Arrays.stream(allQuestion.split(" ")).collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));

        List<DatasetEntity> datasetEntityList = new ArrayList<>();

        wordCount.entrySet().stream()
            .filter(data -> data.getValue() > 3)
            .sorted(Map.Entry.<String, Long> comparingByValue().reversed())
            .forEach(data -> {

                DatasetEntity datasetEntity = new DatasetEntity();
                datasetEntity.setTag(data.getKey());

                questionAnswers.entrySet().stream()
                    .filter(questionAnswer -> questionAnswer.getKey().contains(data.getKey()))
                    .forEach(questionAnswer -> {
                        datasetEntity.getPatterns().add(questionAnswer.getKey());
                        datasetEntity.getResponses().add(questionAnswer.getValue());
                    });

                datasetEntityList.add(datasetEntity);
            });

        System.out.println(datasetEntityList);
    }
}