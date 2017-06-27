package gson;

import bean.Person;
import bean.PersonWithBirthday;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.IOException;

public class GSONReadSample {

    public static void main(String[] args) {
        File file = new File(GSONReadSample.class.
                getResource("/laowang.json").getFile());
        try {
            String content = FileUtils.readFileToString(file, "utf-8");
            Gson gson1 = new Gson();
            Person laowang = gson1.fromJson(content, Person.class);
            System.out.println(laowang);

            Gson gson2 = new GsonBuilder().setDateFormat("yyyy-MM-dd").create();
            PersonWithBirthday laowang_birthday = gson2.fromJson(content, PersonWithBirthday.class);
            System.out.println(laowang_birthday.getBirthday());

            System.out.println(laowang_birthday.getMajor());
            System.out.println(laowang_birthday.getMajor().getClass());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
