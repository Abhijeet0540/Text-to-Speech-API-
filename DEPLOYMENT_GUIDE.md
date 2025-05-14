# Deployment Guide for TTS Interview Website

This guide explains how to deploy your Text-to-Speech Interview Website to GitHub and host it on Vercel or similar platforms.

## 1. Preparing Your Project for GitHub

### Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository (e.g., "interview-tts")
4. Add a description (optional)
5. Choose public or private visibility
6. Click "Create repository"

### Initialize Git in Your Local Project

```bash
# Navigate to your project directory
cd /path/to/your/project

# Initialize git
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit"

# Add the remote repository
git remote add origin https://github.com/your-username/interview-tts.git

# Push to GitHub
git push -u origin main
```

## 2. Deploying to Vercel

### Option 1: Deploy from GitHub

1. Go to [Vercel](https://vercel.com) and sign in (you can sign in with GitHub)
2. Click "Add New..." and select "Project"
3. Import your GitHub repository
4. Configure the project:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: None
   - Output Directory: None
5. Click "Deploy"

### Option 2: Deploy with Vercel CLI

1. Install Vercel CLI:
   ```
   npm install -g vercel
   ```

2. Navigate to your project directory:
   ```
   cd /path/to/your/project
   ```

3. Run the deployment command:
   ```
   vercel
   ```

4. Follow the prompts to configure your project

## 3. Project Structure for Deployment

Your project should have the following structure for successful deployment:

```
interview-tts/
├── api/
│   ├── index.py           # Serverless function for Vercel
│   └── requirements.txt   # Dependencies for the API
├── templates/
│   ├── streaming_index.html
│   └── advanced_index.html
├── static/
│   └── (any static assets)
├── vercel.json            # Vercel configuration
├── requirements.txt       # Main dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
└── (other project files)
```

## 4. Vercel Configuration

The `vercel.json` file configures how Vercel should build and serve your application:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

## 5. Adapting Your Code for Serverless

For Vercel deployment, your Flask application needs to be adapted for serverless functions:

1. Move your main application logic to `api/index.py`
2. Ensure all routes are properly defined
3. Make sure templates and static files are correctly referenced

## 6. Testing Your Deployment

After deployment, Vercel will provide you with a URL (e.g., `https://interview-tts.vercel.app`).

Test your application by:
1. Visiting the URL in your browser
2. Testing the text-to-speech functionality
3. Checking that all features work as expected

## 7. Custom Domain (Optional)

To use a custom domain:

1. Go to your Vercel project dashboard
2. Click "Settings" > "Domains"
3. Add your domain and follow the instructions to configure DNS

## 8. Troubleshooting

### Common Issues:

1. **Missing Dependencies**: Make sure all required packages are in `requirements.txt`
2. **Path Issues**: Ensure paths to templates and static files are correct
3. **API Timeouts**: Vercel has a 10-second timeout for serverless functions
4. **Memory Limits**: Vercel has a 1GB memory limit for serverless functions

### Debugging:

1. Check Vercel deployment logs in your project dashboard
2. Test locally before deploying:
   ```
   vercel dev
   ```

## 9. Integrating with Your Other Projects

To use this TTS service in your other projects:

```javascript
async function speakText(text) {
  try {
    const response = await fetch('https://your-vercel-url.vercel.app/api/stream-speech', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        language: 'en',
        emotion: 'professional'
      }),
    });
    
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    
    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();
    
    // Clean up the URL when done
    audio.onended = () => {
      URL.revokeObjectURL(audioUrl);
    };
  } catch (error) {
    console.error('Error:', error);
  }
}

// Example usage
document.getElementById('speak-button').addEventListener('click', () => {
  const text = document.getElementById('question-text').textContent;
  speakText(text);
});
```

## 10. Maintaining Your Deployment

1. **Updates**: Push changes to GitHub, and Vercel will automatically redeploy
2. **Monitoring**: Check Vercel analytics for usage statistics
3. **Scaling**: Upgrade your Vercel plan if you need more resources
