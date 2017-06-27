package json;

import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class ReadJSONSample {

    public static void main(String[] args) {
        File file = new File(ReadJSONSample.class.
                getResource("/laowang.json").getFile());
        try {
            String content = FileUtils.readFileToString(file, "utf-8");
            JSONObject jsonObject = new JSONObject(content);
            if(!jsonObject.isNull("name"))
                System.out.println("Name: " + jsonObject.getString("name"));
            else
                throw new JSONException("Null key!");

            if(!jsonObject.isNull("nickname"))
                System.out.println("Nickname: " + jsonObject.getString("nickname"));
            else
                throw new JSONException("Null key!");

            System.out.println("Age: " + jsonObject.getInt("age"));
            System.out.println("Has_girlfriend: " + jsonObject.getBoolean("has_girlfriend"));

            JSONArray majorArray = jsonObject.getJSONArray("major");
            for(Object major : majorArray) {
                System.out.println("Major - " + major.toString());
            }
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }
}
