import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  TextField,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Paper,
  Divider,
  Tooltip,
  Alert
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';

const PromptManager = ({ prompts, activePromptId, onPromptAdd, onPromptEdit, onPromptDelete, onPromptActivate }) => {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentPrompt, setCurrentPrompt] = useState({ name: '', content: '' });
  const [error, setError] = useState('');

  const handleOpenDialog = (prompt = null, edit = false) => {
    if (prompt) {
      setCurrentPrompt({ ...prompt });
      setEditMode(edit);
    } else {
      setCurrentPrompt({ name: '', content: '' });
      setEditMode(false);
    }
    setError('');
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
    setCurrentPrompt({ name: '', content: '' });
    setError('');
  };

  const handleSavePrompt = () => {
    // Validate inputs
    if (!currentPrompt.name.trim()) {
      setError('Prompt name is required');
      return;
    }
    if (!currentPrompt.content.trim()) {
      setError('Prompt content is required');
      return;
    }

    if (editMode) {
      onPromptEdit(currentPrompt);
    } else {
      onPromptAdd(currentPrompt);
    }
    handleCloseDialog();
  };

  const handleDeletePrompt = (promptId, isDefault) => {
    if (isDefault) {
      alert('Cannot delete the default prompt');
      return;
    }
    if (window.confirm('Are you sure you want to delete this prompt?')) {
      onPromptDelete(promptId);
    }
  };

  const isDefaultPrompt = (prompt) => prompt.is_default === 1;
  const isActivePrompt = (prompt) => prompt.id === activePromptId;

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">Prompts</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpenDialog()}
        >
          Add Prompt
        </Button>
      </Box>

      <Paper variant="outlined" sx={{ maxHeight: '400px', overflow: 'auto' }}>
        <List>
          {prompts.length === 0 ? (
            <ListItem>
              <ListItemText primary="No prompts available" />
            </ListItem>
          ) : (
            prompts.map((prompt) => (
              <React.Fragment key={prompt.id}>
                <ListItem
                  secondaryAction={
                    <Box>
                      {!isActivePrompt(prompt) && (
                        <Tooltip title="Set as active">
                          <IconButton 
                            edge="end" 
                            onClick={() => onPromptActivate(prompt.id)}
                            sx={{ mr: 1 }}
                          >
                            <RadioButtonUncheckedIcon />
                          </IconButton>
                        </Tooltip>
                      )}
                      {isActivePrompt(prompt) && (
                        <Tooltip title="Active prompt">
                          <IconButton edge="end" sx={{ mr: 1, color: 'primary.main' }}>
                            <CheckCircleIcon />
                          </IconButton>
                        </Tooltip>
                      )}
                      <Tooltip title="Edit prompt">
                        <IconButton 
                          edge="end" 
                          onClick={() => handleOpenDialog(prompt, true)}
                          disabled={isDefaultPrompt(prompt)}
                          sx={{ mr: 1 }}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title={isDefaultPrompt(prompt) ? "Cannot delete default prompt" : "Delete prompt"}>
                        <span>
                          <IconButton
                            edge="end"
                            onClick={() => handleDeletePrompt(prompt.id, isDefaultPrompt(prompt))}
                            disabled={isDefaultPrompt(prompt)}
                          >
                            <DeleteIcon />
                          </IconButton>
                        </span>
                      </Tooltip>
                    </Box>
                  }
                >
                  <ListItemText 
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Typography variant="body1">
                          {prompt.name}
                          {isDefaultPrompt(prompt) && (
                            <Typography 
                              component="span" 
                              variant="caption" 
                              sx={{ ml: 1, color: 'text.secondary' }}
                            >
                              (Default)
                            </Typography>
                          )}
                        </Typography>
                      </Box>
                    }
                    secondary={
                      <Typography 
                        variant="body2" 
                        sx={{ 
                          color: 'text.secondary',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          display: '-webkit-box',
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: 'vertical',
                        }}
                      >
                        {prompt.content.substring(0, 100)}
                        {prompt.content.length > 100 ? '...' : ''}
                      </Typography>
                    }
                  />
                </ListItem>
                <Divider component="li" />
              </React.Fragment>
            ))
          )}
        </List>
      </Paper>

      {/* Add/Edit Prompt Dialog */}
      <Dialog open={dialogOpen} onClose={handleCloseDialog} fullWidth maxWidth="md">
        <DialogTitle>{editMode ? 'Edit Prompt' : 'Add New Prompt'}</DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <TextField
            autoFocus
            margin="dense"
            label="Prompt Name"
            fullWidth
            variant="outlined"
            value={currentPrompt.name}
            onChange={(e) => setCurrentPrompt({ ...currentPrompt, name: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            label="Prompt Content"
            multiline
            rows={10}
            fullWidth
            variant="outlined"
            value={currentPrompt.content}
            onChange={(e) => setCurrentPrompt({ ...currentPrompt, content: e.target.value })}
            placeholder="Enter the system prompt for the AI model..."
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button onClick={handleSavePrompt} variant="contained" color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PromptManager;
