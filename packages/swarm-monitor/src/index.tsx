import React, { useState, useEffect, useRef, memo } from 'react';
import { render, Box, Text, useInput } from 'ink';
import chokidar from 'chokidar';
import fs from 'fs';
import path from 'path';

const COLORS = {
  accent: '#bb9af7',
  focus: '#7aa2f7',
  success: '#9ece6a',
  dim: '#565f89',
  warning: '#e0af68',
  error: '#f7768e',
};

interface Task {
  id: string;
  status: 'pending' | 'in_progress' | 'completed';
  title: string;
}

// Memoized Spinner to prevent full-screen re-renders
const Spinner = memo(() => {
  const [tick, setTick] = useState(0);
  const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
  useEffect(() => {
    const timer = setInterval(() => setTick(t => t + 1), 80);
    return () => clearInterval(timer);
  }, []);
  return <Text color={COLORS.warning}>{frames[tick % frames.length]}</Text>;
});

const Monitor = ({ projectPath }: { projectPath: string }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [logBuffer, setLogBuffer] = useState<string[]>([]);
  const [uptime, setUptime] = useState(0);
  
  const lastLogContent = useRef<string>('');
  const lastTasksHash = useRef<string>('');

  useEffect(() => {
    const timer = setInterval(() => setUptime(u => u + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  useInput((input, key) => {
    if (key.upArrow) setSelectedIndex(prev => Math.max(0, prev - 1));
    if (key.downArrow) setSelectedIndex(prev => Math.min(tasks.length - 1, prev + 1));
  });

  // Registry Watcher with Change Detection
  useEffect(() => {
    const tasksDir = path.join(projectPath, 'tasks');
    const refresh = () => {
      if (!fs.existsSync(tasksDir)) return;
      const files = fs.readdirSync(tasksDir).filter(f => f.endsWith('.json'));
      const raw = files.map(f => {
        try {
          const data = JSON.parse(fs.readFileSync(path.join(tasksDir, f), 'utf-8'));
          return { id: f.replace('.json', ''), status: data.status, title: data.title || f };
        } catch { return null; }
      }).filter(Boolean) as Task[];
      
      const currentHash = JSON.stringify(raw);
      if (currentHash !== lastTasksHash.current) {
        lastTasksHash.current = currentHash;
        setTasks(raw);
      }
    };

    const watcher = chokidar.watch(tasksDir);
    watcher.on('all', refresh);
    refresh();
    return () => { watcher.close(); };
  }, [projectPath]);

  // Log Tailer with Content Comparison
  useEffect(() => {
    const selectedTask = tasks[selectedIndex];
    if (!selectedTask) return;

    const logPaths = [
      `/tmp/worker-${selectedTask.id}.log`,
      `/tmp/actor-orchestrator/worker-${selectedTask.id}.log`
    ];

    const streamLog = () => {
      let foundContent = '';
      for (const p of logPaths) {
        if (fs.existsSync(p)) {
          foundContent = fs.readFileSync(p, 'utf-8');
          break;
        }
      }

      if (foundContent !== lastLogContent.current) {
        lastLogContent.current = foundContent;
        setLogBuffer(foundContent.split('\n').slice(-25));
      } else if (!foundContent && lastLogContent.current !== 'empty') {
        lastLogContent.current = 'empty';
        setLogBuffer([`📡 LISTENING: ${selectedTask.id}...`]);
      }
    };

    const timer = setInterval(streamLog, 500);
    streamLog();
    return () => clearInterval(timer);
  }, [selectedIndex, tasks]);

  return (
    <Box flexDirection="column" paddingX={2} paddingY={1}>
      <Box borderStyle="double" borderColor={COLORS.accent} paddingX={1} marginBottom={1} justifyContent="space-between">
        <Box>
          <Text bold color={COLORS.accent}>🏗️ SOUL </Text>
          <Text bold color="white">MISSION CONTROL</Text>
        </Box>
        <Box>
          <Text color={COLORS.dim}>{Math.floor(uptime/60)}m {uptime%60}s | </Text>
          <Text bold color={COLORS.focus}>Focus: {tasks[selectedIndex]?.id || 'None'}</Text>
        </Box>
      </Box>

      <Box flexDirection="row">
        <Box flexDirection="column" width="40%" borderStyle="round" borderColor={COLORS.dim} paddingX={1}>
          <Text bold color={COLORS.focus}>📋 REGISTRY</Text>
          <Box flexDirection="column" marginTop={1}>
            {tasks.map((task, index) => (
              <Box key={task.id}>
                <Text color={index === selectedIndex ? COLORS.focus : 'white'} bold={index === selectedIndex}>
                  {index === selectedIndex ? '▶ ' : '  '}
                  {task.status === 'completed' ? <Text color={COLORS.success}>✓</Text> : task.status === 'in_progress' ? <Spinner /> : '○'}
                  {' '}{task.id.slice(0, 30)}
                </Text>
              </Box>
            ))}
          </Box>
        </Box>

        <Box flexDirection="column" width="60%" marginLeft={2} borderStyle="round" borderColor={COLORS.focus} paddingX={1} minHeight={28}>
           <Box justifyContent="center" marginBottom={1}>
             <Text bold color={COLORS.accent}>📡 TELEMETRY: {tasks[selectedIndex]?.id || '...'}</Text>
           </Box>
           {logBuffer.map((line, i) => (
             <Text key={i} wrap="truncate-end" color={line.includes('Error') ? COLORS.error : 'white'} dimColor={line.startsWith('>')}>
               {line}
             </Text>
           ))}
        </Box>
      </Box>

      <Box marginTop={1} paddingX={1}>
        <Text color={COLORS.dim}>[↑/↓] Navigate  [CTRL+C] Exit</Text>
      </Box>
    </Box>
  );
};

const projectPath = process.argv[2] || '.';
render(<Monitor projectPath={path.resolve(projectPath)} />);
