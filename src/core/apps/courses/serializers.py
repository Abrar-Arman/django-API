from rest_framework import serializers
from .models import Category, Course, Lesson,Enroll,LessonProgress

# ----------------------
# Lesson Serializer
# ----------------------
class LessonSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course', 
        write_only=True
    )
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'order', 'video_file', 'document_file','course_id']

    def validate_video_file(self, value):
        if value:
            if not value.name.lower().endswith(('.mp4', '.mov', '.avi')):
                raise serializers.ValidationError(
                    "Video must be MP4, MOV, or AVI."
                )
        return value

    def validate_document_file(self, value):
        if value:
            if not value.name.lower().endswith(('.pdf', '.docx')):
                raise serializers.ValidationError(
                    "Document must be PDF or DOCX."
                )
        return value


# ----------------------
# Course Serializer 
# ----------------------

class CourseSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category', 
        write_only=True
    )

    id = serializers.ReadOnlyField()
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'level', 'category_id', 'created_by']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
    

class CourseDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'level', 'created_by', 'lessons']

    def get_lessons(self, obj):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if user and user.is_authenticated and obj.created_by == user:
            return LessonSerializer(obj.lessons.all(), many=True, context=self.context).data

        if user and user.is_authenticated:
            if obj.registrations.filter(user=user, status='confirmed').exists():
                return LessonSerializer(obj.lessons.all(), many=True, context=self.context).data

        first_lesson = obj.lessons.order_by('order').first()
        if first_lesson:
            return [LessonSerializer(first_lesson, context=self.context).data]

        return []





# ----------------------
# Category Serializers
# ----------------------
class CategoryListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class CategoryDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    courses = CourseSerializer(source='course_set', many=True, read_only=True) 

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'courses']


# ----------------------
# Enroll Serializers
# ----------------------


class EnrollSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    course=serializers.StringRelatedField(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course',  
        write_only=True
    )

    class Meta:
        model = Enroll
        fields = ['id', 'user', 'course', 'course_id', 'status', 'registered_at']
        read_only_fields = ['id','user', 'course', 'status', 'registered_at']


# ----------------------
# progrss Serializers
# ----------------------

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = []  

    def create(self, validated_data):
        user = self.context['user']
        lesson = self.context['lesson']

        progress, created = LessonProgress.objects.get_or_create(user=user, lesson=lesson)
        if not created:
            progress.delete()
            return {"action": "unmarked"}  
        return {"action": "marked"}  

class LessonProgressListSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    course_title = serializers.CharField(source='lesson.course.title', read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)
    completion_percentage = serializers.SerializerMethodField()


    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson_title', 'course_title', 'completed_at','completion_percentage']
    
    
    def get_completion_percentage(self, obj):
       
        course = obj.lesson.course
        user = obj.user

        total_lessons = course.lessons.count()
        if total_lessons == 0:
            return 0

        completed_lessons = LessonProgress.objects.filter(
            user=user,
            lesson__course=course
        ).count()

        return round((completed_lessons / total_lessons) * 100, 2)