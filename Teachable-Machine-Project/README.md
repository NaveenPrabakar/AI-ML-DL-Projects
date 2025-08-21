# Thumbs Up/Down Detection

A simple computer vision project using Google's Teachable Machine to detect and classify thumbs up and thumbs down gestures in real-time.

## Overview

This project uses a trained machine learning model to recognize hand gestures:
- 👍 **Thumbs Up**: Positive gesture detection
- 👎 **Thumbs Down**: Negative gesture detection

Built with Google's Teachable Machine platform for easy training and deployment.


## Training Data

Model trained on:
- **Thumbs Up**: 50+ images of various angles and lighting
- **Thumbs Down**: 50+ images with different hand positions
- **Background**: Control images without gestures
```

## Performance

- **Accuracy**: ~95% on test gestures
- **Speed**: Real-time detection at 30fps
- **Model Size**: <5MB for fast loading

## Customization

Want to add more gestures? 
1. Visit [teachablemachine.withgoogle.com](https://teachablemachine.withgoogle.com)
2. Create new image classification project
3. Add your gesture classes
4. Train and export the model
5. Replace model files in this project

---
*Built with ❤️ using Google Teachable Machine*