from rest_framework import serializers
from .models import Profile,File,DataUpload
from .views import validate_file_extension, validate_csv_file, Exist_file
import pandas as pd
from django.contrib import messages

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        # fields='__all__'
        fields=('first_name','last_name',
                 
                'username',
                'email',
                'gender', 
                'date_of_birth',
                'mobile_number',
                'user'
                )



class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

    def validate_file(self, value):
        validate_file_extension(value)
        return value

    def validate(self, data):
        file_name = data['file'].name
        if File.objects.filter(file__icontains=file_name).exists():
            raise serializers.ValidationError("A file with the same name already exists.")
        return data

    def create(self, validated_data):
        file = validated_data.pop('file')
        validate_csv_file(file)
        instance = File.objects.create(file=file, **validated_data)
        return instance
    



class DataUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = DataUpload
        fields = ['file']

    def validate_file(self, value):
        validate_file_extension(value)
        return value


    def create(self, validated_data):
        # Access authenticated user from request
        user = self.context['request'].user

        file = validated_data.pop('file')

        try:
            # Validate CSV file
            csvfile = validate_csv_file(file)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

        try:
            reader = pd.read_csv(csvfile)

            # Ensure that 'cl1' and 'cl2' columns exist in the CSV file
            required_columns = ['cl1', 'cl2']
            if not all(col in reader.columns for col in required_columns):
                raise serializers.ValidationError('Columns "cl1" and "cl2" are required.')

            instances = []
            for index, row in reader.iterrows():
                # Create DataUpload instance for each row in the CSV file
                instance = DataUpload(cl1=row['cl1'], cl2=row['cl2'], user=user)
                instances.append(instance)

            # Bulk create DataUpload instances
            DataUpload.objects.bulk_create(instances)

            # Return success message
            messages.success(self.context['request'], "File uploaded successfully.")
        except Exception as e:
            raise serializers.ValidationError(f"Something went wrong: {str(e)}")

        return validated_data