package maks.ter;

import lombok.Data;

import java.util.ArrayList;
import java.util.List;

public class DatasetEntity {
    private String tag;
    private List<String> patterns = new ArrayList<>();
    private List<String> responses = new ArrayList<>();

    public String getTag() {
        return tag;
    }

    public void setTag(String tag) {
        this.tag = tag;
    }

    public List<String> getPatterns() {
        return patterns;
    }

    public void setPatterns(List<String> patterns) {
        this.patterns = patterns;
    }

    public List<String> getResponses() {
        return responses;
    }

    public void setResponses(List<String> responses) {
        this.responses = responses;
    }

    @Override
    public String toString() {
        return "DatasetEntity{" +
                "tag='" + tag + '\'' +
                ", patterns=" + patterns +
                ", responses=" + responses +
                '}';
    }
}
