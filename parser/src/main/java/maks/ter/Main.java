package maks.ter;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.function.Function;
import java.util.stream.Collectors;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

public class Main {

    private static HashMap<String, String[]> tags = new HashMap<>() {{
        put("���������", "��������, �������, ��������, ������, �����, �����, �������, ������, ��������, ������, ������, ������, �����, ��������, ���, ������, ������".split(", "));
        put("�����������", "������, ������, �����������, ���, ���, �����, ������, �����, �������, ������, ���, �������, ������, ������, ������".split(", "));
        put("��������", "������������, ���������, �������, ��������, ����, ������, ����, ����, ���, �������".split(", "));
        put("���������", "�������, ���������, �������, ���, �����, �������, �������".split(", "));
        put("����������� ��������", "��������, ��������, ���, ���".split(", "));
        put("��������", "���, ���, ������, �������, ������".split(", "));
        put("�������", "��������, �������".split(", "));
        put("������", "�����, �����, �������, �����, ���, ������, ������, ��������".split(", "));
        put("����������� �����������", "�������, �������, �����, ���, �����, ������, �����, ����, �����, �����, ������, ����������".split(", "));
        put("��������", "�����, �����, ������".split(", "));
    }};

    public static void main(String[] args) {
        List<QuestionAnswer> resultSet = DatabaseService.createSession().openSession().createQuery("FROM QuestionAnswer").list();

        List<QuestionAnswer> questionAnswers = new ArrayList<QuestionAnswer>();
        Set<String> titles = new HashSet<>();

        for(QuestionAnswer item : resultSet) {
            if (titles.add(item.getQuestion())) {
                questionAnswers.add(item);
            }
        }

        List<DatasetEntity> datasetEntityList = new ArrayList<>();
        for (var tagData: tags.entrySet()) {
            DatasetEntity datasetEntity = new DatasetEntity();
            datasetEntity.setTag(tagData.getKey());
            datasetEntity.setPatterns(new ArrayList<>());
            datasetEntity.setResponses(new ArrayList<>());

            for (var questionAnswer: questionAnswers) {
                if (Arrays.stream(tagData.getValue()).anyMatch(tag -> questionAnswer.getQuestion().toLowerCase().contains(tag.toLowerCase()))) {
                    datasetEntity.getPatterns().add(questionAnswer.getQuestion());
                    datasetEntity.getResponses().add(questionAnswer.getAnswer());
                }
            }

            datasetEntityList.add(datasetEntity);
        }

        HashMap<String, List<Object>> jsonObject = new HashMap<>();
        jsonObject.put("intents", Collections.singletonList(datasetEntityList));
        ObjectMapper mapper = new ObjectMapper();
        try {
            // Writing to a file
            mapper.writeValue(new File("C:\\workspace\\backend\\neuro-chat-bot\\parser\\src\\main\\resources\\intense.json"), jsonObject);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}