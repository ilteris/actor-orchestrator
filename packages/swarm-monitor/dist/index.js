import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect, useRef, memo } from 'react';
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
// Memoized Spinner to prevent full-screen re-renders
const Spinner = memo(() => {
    const [tick, setTick] = useState(0);
    const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
    useEffect(() => {
        const timer = setInterval(() => setTick(t => t + 1), 80);
        return () => clearInterval(timer);
    }, []);
    return _jsx(Text, { color: COLORS.warning, children: frames[tick % frames.length] });
});
const Monitor = ({ projectPath }) => {
    const [tasks, setTasks] = useState([]);
    const [selectedIndex, setSelectedIndex] = useState(0);
    const [logBuffer, setLogBuffer] = useState([]);
    const [uptime, setUptime] = useState(0);
    const lastLogContent = useRef('');
    const lastTasksHash = useRef('');
    useEffect(() => {
        const timer = setInterval(() => setUptime(u => u + 1), 1000);
        return () => clearInterval(timer);
    }, []);
    useInput((input, key) => {
        if (key.upArrow)
            setSelectedIndex(prev => Math.max(0, prev - 1));
        if (key.downArrow)
            setSelectedIndex(prev => Math.min(tasks.length - 1, prev + 1));
    });
    // Registry Watcher with Change Detection
    useEffect(() => {
        const tasksDir = path.join(projectPath, 'tasks');
        const refresh = () => {
            if (!fs.existsSync(tasksDir))
                return;
            const files = fs.readdirSync(tasksDir).filter(f => f.endsWith('.json'));
            const raw = files.map(f => {
                try {
                    const data = JSON.parse(fs.readFileSync(path.join(tasksDir, f), 'utf-8'));
                    return { id: f.replace('.json', ''), status: data.status, title: data.title || f };
                }
                catch {
                    return null;
                }
            }).filter(Boolean);
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
        if (!selectedTask)
            return;
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
            }
            else if (!foundContent && lastLogContent.current !== 'empty') {
                lastLogContent.current = 'empty';
                setLogBuffer([`📡 LISTENING: ${selectedTask.id}...`]);
            }
        };
        const timer = setInterval(streamLog, 500);
        streamLog();
        return () => clearInterval(timer);
    }, [selectedIndex, tasks]);
    return (_jsxs(Box, { flexDirection: "column", paddingX: 2, paddingY: 1, children: [_jsxs(Box, { borderStyle: "double", borderColor: COLORS.accent, paddingX: 1, marginBottom: 1, justifyContent: "space-between", children: [_jsxs(Box, { children: [_jsx(Text, { bold: true, color: COLORS.accent, children: "\uD83C\uDFD7\uFE0F SOUL " }), _jsx(Text, { bold: true, color: "white", children: "MISSION CONTROL" })] }), _jsxs(Box, { children: [_jsxs(Text, { color: COLORS.dim, children: [Math.floor(uptime / 60), "m ", uptime % 60, "s | "] }), _jsxs(Text, { bold: true, color: COLORS.focus, children: ["Focus: ", tasks[selectedIndex]?.id || 'None'] })] })] }), _jsxs(Box, { flexDirection: "row", children: [_jsxs(Box, { flexDirection: "column", width: "40%", borderStyle: "round", borderColor: COLORS.dim, paddingX: 1, children: [_jsx(Text, { bold: true, color: COLORS.focus, children: "\uD83D\uDCCB REGISTRY" }), _jsx(Box, { flexDirection: "column", marginTop: 1, children: tasks.map((task, index) => (_jsx(Box, { children: _jsxs(Text, { color: index === selectedIndex ? COLORS.focus : 'white', bold: index === selectedIndex, children: [index === selectedIndex ? '▶ ' : '  ', task.status === 'completed' ? _jsx(Text, { color: COLORS.success, children: "\u2713" }) : task.status === 'in_progress' ? _jsx(Spinner, {}) : '○', ' ', task.id.slice(0, 30)] }) }, task.id))) })] }), _jsxs(Box, { flexDirection: "column", width: "60%", marginLeft: 2, borderStyle: "round", borderColor: COLORS.focus, paddingX: 1, minHeight: 28, children: [_jsx(Box, { justifyContent: "center", marginBottom: 1, children: _jsxs(Text, { bold: true, color: COLORS.accent, children: ["\uD83D\uDCE1 TELEMETRY: ", tasks[selectedIndex]?.id || '...'] }) }), logBuffer.map((line, i) => (_jsx(Text, { wrap: "truncate-end", color: line.includes('Error') ? COLORS.error : 'white', dimColor: line.startsWith('>'), children: line }, i)))] })] }), _jsx(Box, { marginTop: 1, paddingX: 1, children: _jsx(Text, { color: COLORS.dim, children: "[\u2191/\u2193] Navigate  [CTRL+C] Exit" }) })] }));
};
const projectPath = process.argv[2] || '.';
render(_jsx(Monitor, { projectPath: path.resolve(projectPath) }));
